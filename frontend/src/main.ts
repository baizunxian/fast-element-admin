import {createApp} from 'vue';
import pinia from '/@/stores/index';
import App from './App.vue';
import router from './router';
import {directive} from '/@/directive/index';
import other from '/@/utils/other';

import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import '/@/theme/index.scss';

const app = createApp(App);

directive(app);
other.apiPublicAssembly(app)

app.use(pinia).use(router).use(ElementPlus).mount('#app');
