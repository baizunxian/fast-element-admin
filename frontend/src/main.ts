import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { directive } from '/@/directive/index';
import other from '/@/utils/other';

import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import '/@/theme/index.scss';
import { initStores } from "/@/stores";

async function initApplication() {
	const app = createApp(App);

	const namespace = `${import.meta.env.VITE_APP_NAMESPACE}`;
	await initStores(app, { namespace })

	directive(app);
	other.apiPublicAssembly(app)
	app.use(router)
	app.use(ElementPlus)
	app.mount('#app');
}

initApplication()