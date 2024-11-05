import {Local} from '/@/utils/storage';
import {useThemeConfig} from "/@/stores/themeConfig";
import {storeToRefs} from "pinia";
import {computed, nextTick} from "vue";
import {getDarkColor, getHexColor, getLightColor} from "/@/utils/theme";
import mittBus from "/@/utils/mitt";
import Watermark from "/@/utils/watermark";
import {verifyAndSpace} from "/@/utils/toolsValidate";
import {copyText} from "/@/utils";


export const storesThemeConfig = useThemeConfig();
export const {themeConfig}: { themeConfig: RefType<any> } = storeToRefs(storesThemeConfig);


// 获取布局配置信息
export const getThemeConfig = computed(() => {
	return themeConfig.value;
});
// 存储布局配置
// export const setLocalThemeConfig = () => {
// 	Local.remove('themeConfig');
// 	Local.set('themeConfig', getThemeConfig.value);
// };
// 存储布局配置全局主题样式（html根标签）
// export const setLocalThemeConfigStyle = () => {
// 	Local.set('themeConfigStyle', document.documentElement.style.cssText);
// };


// 触发 store 布局配置更新
export const setDispatchThemeConfig = () => {
	setLocalThemeConfig();
	setLocalThemeConfigStyle();
};


// 1、全局主题
export const onColorPickerChange = (color?: string) => {
	if (!color) return "";
	const hexColor = getHexColor(color)
	getThemeConfig.value.primary = hexColor;
	const darkColor = getDarkColor(hexColor, 0.1);
	// 颜色加深
	document.documentElement.style.setProperty('--el-color-primary-dark-2', `${darkColor}`);
	document.documentElement.style.setProperty('--el-color-primary', getThemeConfig.value.primary);
	// 颜色变浅
	for (let i = 1; i <= 9; i++) {
		document.documentElement.style.setProperty(`--el-color-primary-light-${i}`, `${getLightColor(getThemeConfig.value.primary, i / 10)}`);
	}
	setDispatchThemeConfig();
};

// 2、菜单 / 顶栏
export const onBgColorPickerChange = (bg: string) => {
	document.documentElement.style.setProperty(`--next-bg-${bg}`, themeConfig.value[bg]);
	if (bg === 'menuBar') {
		document.documentElement.style.setProperty(`--next-bg-menuBar-light-1`, getLightColor(getThemeConfig.value.menuBar, 0.05));
	}
	onTopBarGradualChange();
	onMenuBarGradualChange();
	onColumnsMenuBarGradualChange();
	setDispatchThemeConfig();
};
// 2、菜单 / 顶栏 --> 顶栏背景渐变
export const onTopBarGradualChange = () => {
	setGraduaFun('.layout-navbars-breadcrumb-index', getThemeConfig.value.isTopBarColorGradual, getThemeConfig.value.topBar);
};
// 2、菜单 / 顶栏 --> 菜单背景渐变
export const onMenuBarGradualChange = () => {
	setGraduaFun('.layout-container .el-aside', getThemeConfig.value.isMenuBarColorGradual, getThemeConfig.value.menuBar);
};
// 2、菜单 / 顶栏 --> 分栏菜单背景渐变
export const onColumnsMenuBarGradualChange = () => {
	setGraduaFun('.layout-container .layout-columns-aside', getThemeConfig.value.isColumnsMenuBarColorGradual, getThemeConfig.value.columnsMenuBar);
};
// 2、菜单 / 顶栏 --> 背景渐变函数
export const setGraduaFun = (el: any, bool: boolean, color: string) => {
	nextTick(() => {
		setTimeout(() => {
			let els = document.querySelector(el);
			if (!els) return false;
			document.documentElement.style.setProperty('--el-menu-bg-color', document.documentElement.style.getPropertyValue('--next-bg-menuBar'));
			if (bool) els.setAttribute('style', `background:linear-gradient(to bottom , ${color}, ${getLightColor(color, 0.5)})`);
			else els.setAttribute('style', ``);
			setLocalThemeConfig();
		}, 300);
	});
};

// 3、界面设置 --> 菜单水平折叠
export const onThemeConfigChange = () => {
	setDispatchThemeConfig();
};
// 3、界面设置 --> 固定 Header
export const onIsFixedHeaderChange = () => {
	getThemeConfig.value.isFixedHeaderChange = getThemeConfig.value.isFixedHeader ? false : true;
	setLocalThemeConfig();
};
// 3、界面设置 --> 经典布局分割菜单
export const onClassicSplitMenuChange = () => {
	getThemeConfig.value.isBreadcrumb = false;
	setLocalThemeConfig();
	mittBus.emit('getBreadcrumbIndexSetFilterRoutes');
};
// 4、界面显示 --> 侧边栏 Logo
export const onIsShowLogoChange = () => {
	getThemeConfig.value.isShowLogoChange = getThemeConfig.value.isShowLogo ? false : true;
	setLocalThemeConfig();
};
// 4、界面显示 --> 面包屑 Breadcrumb
export const onIsBreadcrumbChange = () => {
	if (getThemeConfig.value.layout === 'classic') {
		getThemeConfig.value.isClassicSplitMenu = false;
	}
	setLocalThemeConfig();
};
// 4、界面显示 --> 开启 TagsView 拖拽
export const onSortableTagsViewChange = () => {
	mittBus.emit('openOrCloseSortable');
	setLocalThemeConfig();
};
// 4、界面显示 --> 开启 TagsView 共用
export const onShareTagsViewChange = () => {
	mittBus.emit('openShareTagsView');
	setLocalThemeConfig();
};
// 4、界面显示 --> 灰色模式/色弱模式
export const onAddFilterChange = (attr: string) => {
	if (attr === 'grayscale') {
		if (getThemeConfig.value.isGrayscale) getThemeConfig.value.isInvert = false;
	} else {
		if (getThemeConfig.value.isInvert) getThemeConfig.value.isGrayscale = false;
	}
	const cssAttr =
		attr === 'grayscale' ? `grayscale(${getThemeConfig.value.isGrayscale ? 1 : 0})` : `invert(${getThemeConfig.value.isInvert ? '80%' : '0%'})`;
	const appEle = document.body;
	appEle.setAttribute('style', `filter: ${cssAttr}`);
	setLocalThemeConfig();
};

// 4、界面显示 --> 开启水印
export const onWartermarkChange = () => {
	getThemeConfig.value.isWartermark ? Watermark.set(getThemeConfig.value.wartermarkText) : Watermark.del();
	setLocalThemeConfig();
};
// 4、界面显示 --> 水印文案
export const onWartermarkTextInput = (val: any) => {
	getThemeConfig.value.wartermarkText = verifyAndSpace(val);
	if (getThemeConfig.value.wartermarkText === '') return false;
	if (getThemeConfig.value.isWartermark) Watermark.set(getThemeConfig.value.wartermarkText);
	setLocalThemeConfig();
};
// 5、布局切换
export const onSetLayout = (layout: string) => {
	Local.set('oldLayout', layout);
	if (getThemeConfig.value.layout === layout) return false;
	if (layout === 'transverse') getThemeConfig.value.isCollapse = false;
	getThemeConfig.value.layout = layout;
	// getThemeConfig.value.isDrawer = false;
	initLayoutChangeFun();
};
// 设置布局切换函数
export const initLayoutChangeFun = () => {
	onBgColorPickerChange('menuBar');
	onBgColorPickerChange('menuBarColor');
	onBgColorPickerChange('menuBarActiveColor');
	onBgColorPickerChange('topBar');
	onBgColorPickerChange('topBarColor');
	onBgColorPickerChange('columnsMenuBar');
	onBgColorPickerChange('columnsMenuBarColor');
};
// 关闭弹窗时，初始化变量。变量用于处理 layoutScrollbarRef.value.update() 更新滚动条高度
export const onDrawerClose = () => {
	getThemeConfig.value.isFixedHeaderChange = false;
	getThemeConfig.value.isShowLogoChange = false;
	getThemeConfig.value.isDrawer = false;
	setLocalThemeConfig();
};
// 布局配置弹窗打开
export const openDrawer = () => {
	getThemeConfig.value.isDrawer = true;
};
// 存储布局配置
export const setLocalThemeConfig = () => {
	Local.remove('themeConfig');
	Local.set('themeConfig', getThemeConfig.value);
};
// 存储布局配置全局主题样式（html根标签）
export const setLocalThemeConfigStyle = () => {
	Local.set('themeConfigStyle', document.documentElement.style.cssText);
};
// 一键复制配置
export const onCopyConfigClick = () => {
	let copyThemeConfig = Local.get('themeConfig');
	copyThemeConfig.isDrawer = false;
	copyText(JSON.stringify(copyThemeConfig)).then(() => {
		getThemeConfig.value.isDrawer = false;
	});
};
// 一键恢复默认
export const onResetConfigClick = () => {
	Local.clear();
	window.location.reload();
	// @ts-ignore
	Local.set('version', __NEXT_VERSION__);
};
// 初始化菜单样式等
export const initSetStyle = () => {
	// 2、菜单 / 顶栏 --> 顶栏背景渐变
	onTopBarGradualChange();
	// 2、菜单 / 顶栏 --> 菜单背景渐变
	onMenuBarGradualChange();
	// 2、菜单 / 顶栏 --> 分栏菜单背景渐变
	onColumnsMenuBarGradualChange();
};

export const onColumnsMenuHoverPreloadChange = () => {
	setLocalThemeConfig();
};


// 4、界面显示 --> 深色模式
export const onAddDarkChange = (theme?: string) => {
	const body = document.documentElement;
	switch (theme) {
		case 'dark':
			body.setAttribute('data-theme', 'dark');
			getThemeConfig.value.isIsDark = true
			break;
		default:
			body.setAttribute('data-theme', '');
			getThemeConfig.value.isIsDark = false;
	}
	setDispatchThemeConfig()
};