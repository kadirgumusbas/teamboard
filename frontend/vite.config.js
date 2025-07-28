import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vueDevTools(
            {
                launchEditor: 'pycharm'
            }
        ),
        vue()],
    server: {
        proxy: {
            '/api': 'http://127.0.0.1:8000', // Django backend adresin neyse o
        }
    }
})
