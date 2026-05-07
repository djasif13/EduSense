from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
import hashlib, json, time
from jose import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

router = APIRouter()

LTI_CLIENT_ID = "edusense_client_001"
LTI_PLATFORM_URL = "http://localhost:3333"

def get_private_key():
    with open("lti_private.pem", "rb") as f:
        return f.read()

def get_public_key():
    with open("lti_public.pem", "rb") as f:
        return serialization.load_pem_public_key(f.read(), backend=default_backend())

@router.post("/lti/login")
async def lti_login(request: Request):
    form = await request.form()
    login_hint = form.get("login_hint", "")
    redirect_uri = form.get("target_link_uri", "http://localhost:3333/")
    nonce = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
    state = hashlib.sha256(login_hint.encode()).hexdigest()[:16]
    auth_url = (
        f"{LTI_PLATFORM_URL}/lti/authorize"
        f"?response_type=id_token"
        f"&client_id={LTI_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&login_hint={login_hint}"
        f"&nonce={nonce}"
        f"&state={state}"
        f"&scope=openid"
        f"&response_mode=form_post"
    )
    return RedirectResponse(auth_url)

@router.post("/lti/launch")
async def lti_launch(request: Request):
    form = await request.form()
    id_token = form.get("id_token", "")
    try:
        claims = jwt.decode(id_token, get_private_key(), algorithms=["RS256"], options={"verify_signature": False})
        user_sub = claims.get("sub", "anonymous")
        learner_id = hashlib.sha256(user_sub.encode()).hexdigest()[:16]
        roles = claims.get("https://purl.imsglobal.org/spec/lti/claim/roles", [])
        return JSONResponse({
            "learner_id": learner_id,
            "roles": roles,
            "session_ready": True
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

@router.get("/lti/jwks")
async def lti_jwks():
    from cryptography.hazmat.primitives.asymmetric import rsa
    from jose import jwk
    pub = get_public_key()
    pub_pem = pub.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
    key = jwk.construct(pub_pem, algorithm="RS256")
    return JSONResponse({"keys": [key.to_dict()]})

@router.post("/lti/token")
async def lti_token(request: Request):
    return JSONResponse({"access_token": "stub_token", "token_type": "bearer", "expires_in": 3600})
