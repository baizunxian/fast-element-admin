import {ElMessage} from 'element-plus';

/**
 * 颜色转换函数
 * @method hexToRgb hex 颜色转 rgb 颜色
 * @method rgbToHex rgb 颜色转 Hex 颜色
 * @method getDarkColor 加深颜色值
 * @method getLightColor 变浅颜色值
 */
export function useChangeColor() {

	const strHslToRgb = (str: string): any => {
		const regex = /^hsl\((\d+)(?:deg)?\s*,\s*(\d+)%\s*,\s*(\d+)%\s*\)$/i;
		const matches = str.match(regex);

		// 辅助函数，用于计算 RGB 的各个分量
		function hue2rgb(p: number, q: number, t: number) {
			if (t < 0) t += 1;
			if (t > 1) t -= 1;
			if (t < 1 / 6) return p + (q - p) * 6 * t;
			if (t < 1 / 2) return q;
			if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
			return p;
		}


		if (matches) {
			let h = parseInt(matches[1], 10); // hue
			let s = parseInt(matches[2], 10); // saturation
			let l = parseInt(matches[3], 10); // lightness
			h /= 360;
			s /= 100;
			l /= 100;

			let q = l < 0.5 ? l * (1 + s) : l + s - l * s;
			let p = 2 * l - q;

			const r = Math.round(hue2rgb(p, q, h + 1 / 3) * 255);
			const g = Math.round(hue2rgb(p, q, h) * 255);
			const b = Math.round(hue2rgb(p, q, h - 1 / 3) * 255);

			return [r, g, b];
		} else {
			throw new Error('输入错误的hsl');
		}
	};

	// str 颜色值字符串
	const hexToRgb = (str: string): any => {
		let hexs: any = '';
		let reg = /^\#?[0-9A-Fa-f]{6}$/;
		if (!reg.test(str)) {
			ElMessage.warning('输入错误的hex');
			return '';
		}
		str = str.replace('#', '');
		hexs = str.match(/../g);
		for (let i = 0; i < 3; i++) hexs[i] = parseInt(hexs[i], 16);
		return hexs;
	};
	// r 代表红色 | g 代表绿色 | b 代表蓝色
	const rgbToHex = (r: any, g: any, b: any): string => {
		let reg = /^\d{1,3}$/;
		if (!reg.test(r) || !reg.test(g) || !reg.test(b)) {
			ElMessage.warning('输入错误的rgb颜色值');
			return '';
		}
		let hexs = [r.toString(16), g.toString(16), b.toString(16)];
		for (let i = 0; i < 3; i++) if (hexs[i].length == 1) hexs[i] = `0${hexs[i]}`;
		return `#${hexs.join('')}`;
	};
	// color 颜色值字符串 | level 变浅的程度，限0-1之间
	const getDarkColor = (color: string, level: number): string => {
		let reg = /^\#?[0-9A-Fa-f]{6}$/;
		if (!reg.test(color)) {
			ElMessage.warning('输入错误的hex颜色值');
			return '';
		}
		let rgb = useChangeColor().hexToRgb(color);
		for (let i = 0; i < 3; i++) rgb[i] = Math.floor(rgb[i] * (1 - level));
		return useChangeColor().rgbToHex(rgb[0], rgb[1], rgb[2]);
	};
	// color 颜色值字符串 | level 加深的程度，限0-1之间
	const getLightColor = (color: string, level: number): string => {
		let reg = /^\#?[0-9A-Fa-f]{6}$/;
		if (!reg.test(color)) {
			ElMessage.warning('输入错误的hex颜色值');
			return '';
		}
		let rgb = useChangeColor().hexToRgb(color);
		for (let i = 0; i < 3; i++) rgb[i] = Math.floor((255 - rgb[i]) * level + rgb[i]);
		return useChangeColor().rgbToHex(rgb[0], rgb[1], rgb[2]);
	};

	return {
		hexToRgb,
		rgbToHex,
		getDarkColor,
		getLightColor,
	};
}


export const hslToRgb = (h: number, s: number, l: number): Array<number> => {

	// 辅助函数，用于计算 RGB 的各个分量
	function hue2rgb(p: number, q: number, t: number) {
		if (t < 0) t += 1;
		if (t > 1) t -= 1;
		if (t < 1 / 6) return p + (q - p) * 6 * t;
		if (t < 1 / 2) return q;
		if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
		return p;
	}

	h /= 360;
	s /= 100;
	l /= 100;

	let q = l < 0.5 ? l * (1 + s) : l + s - l * s;
	let p = 2 * l - q;

	const r = Math.round(hue2rgb(p, q, h + 1 / 3) * 255);
	const g = Math.round(hue2rgb(p, q, h) * 255);
	const b = Math.round(hue2rgb(p, q, h - 1 / 3) * 255);

	return [r, g, b];

}

// str 颜色值字符串
export const hexToRgb = (str: string): any => {
	let hexs: any = '';
	let reg = /^\#?[0-9A-Fa-f]{6}$/;
	if (!reg.test(str)) {
		ElMessage.warning('输入错误的hex');
		return '';
	}
	str = str.replace('#', '');
	hexs = str.match(/../g);
	for (let i = 0; i < 3; i++) hexs[i] = parseInt(hexs[i], 16);
	return hexs;
}
// r 代表红色 | g 代表绿色 | b 代表蓝色
export const rgbToHex = (r: any, g: any, b: any): string => {
	let reg = /^\d{1,3}$/;
	if (!reg.test(r) || !reg.test(g) || !reg.test(b)) {
		ElMessage.warning('输入错误的rgb颜色值');
		return '';
	}
	let hexs = [r.toString(16), g.toString(16), b.toString(16)];
	for (let i = 0; i < 3; i++) if (hexs[i].length == 1) hexs[i] = `0${hexs[i]}`;
	return `#${hexs.join('')}`;
};
// color 颜色值字符串 | level 变浅的程度，限0-1之间
export const getDarkColor = (color: string, level: number): string => {
	const hexTColor = getHexColor(color)
	let rgb = hexToRgb(hexTColor);
	for (let i = 0; i < 3; i++) rgb[i] = Math.floor(rgb[i] * (1 - level));
	return rgbToHex(rgb[0], rgb[1], rgb[2]);
};
// color 颜色值字符串 | level 加深的程度，限0-1之间
export const getLightColor = (color: string, level: number): string => {
	const hexTColor = getHexColor(color)
	let rgb = hexToRgb(hexTColor);
	for (let i = 0; i < 3; i++) rgb[i] = Math.floor((255 - rgb[i]) * level + rgb[i]);
	return rgbToHex(rgb[0], rgb[1], rgb[2]);
}

export const getHexColor = (color: string): string => {
	// 正则表达式用于匹配 HEX 颜色
	const hexColorPattern = /^#([0-9A-F]{3}){1,2}$/i;
	// 正则表达式用于匹配 RGB(A) 颜色
	const rgbColorPattern = /^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$/;
	const rgbaColorPattern = /^rgba\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(0|1|0?\.\d+)\s*\)$/;
	// 正则表达式用于匹配 HSL(A) 颜色
	const hslColorPattern = /^hsl\(\s*(\d{1,3})\s*[\s,]*(\d{1,3})%\s*[\s,]*(\d{1,3})%\s*\)$/;
	const hslaColorPattern = /^hsla\(\s*(\d{1,3})\s*,\s*(\d{1,3})%\s*,\s*(\d{1,3})%\s*,\s*(0|1|0?\.\d+)\s*\)$/;
	// 检查 HEX 颜色
	if (hexColorPattern.test(color)) {
		return color;
	}
	// 检查 RGB 颜色
	if (rgbColorPattern.test(color)) {
		const matches = color.match(rgbColorPattern);
		if (matches) {
			// 提取并返回 RGB 值
			const r = parseInt(matches[1], 10);
			const g = parseInt(matches[2], 10);
			const b = parseInt(matches[3], 10);
			return useChangeColor().rgbToHex(r, g, b);
		} else {
			ElMessage.warning('输入错误的颜色值');
			throw new Error('输入错误的颜色值');
		}
	}
	// 检查 RGBA 颜色
	// if (rgbaColorPattern.test(color)) {
	// 	return true;
	// }
	// 检查 HSL 颜色
	if (hslColorPattern.test(color)) {
		const matches = color.match(hslColorPattern);
		if (matches) {
			let h = parseInt(matches[1], 10); // hue
			let s = parseInt(matches[2], 10); // saturation
			let l = parseInt(matches[3], 10); // lightness
			const rbg: number[] = hslToRgb(h, s, l)
			// @ts-ignore
			return rgbToHex(...rbg)
		} else {
			ElMessage.warning('输入错误的hsl');
			throw new Error('输入错误的hsl');
		}

	}
	// 检查 HSLA 颜色
	// if (hslaColorPattern.test(color)) {
	// 	return true;
	// }
	// 如果没有匹配任何颜色格式，返回 false
	ElMessage.warning('输入错误的颜色值');
	throw new Error('输入错误的颜色值');
}