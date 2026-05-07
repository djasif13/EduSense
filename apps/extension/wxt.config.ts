import { defineConfig } from 'wxt';

export default defineConfig({
  extensionApi: 'chrome',
  modules: ['@wxt-dev/module-react'],
  manifest: {
    name: 'EduSense',
    description: 'Privacy-first learning friction intelligence',
    permissions: ['tabs', 'storage', 'scripting'],
    host_permissions: ['<all_urls>']
  }
});
