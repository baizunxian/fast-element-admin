export function handlerRedirectUrl() {
	try {
		let localUrl = window.location.href.replace("/#", '');
		const newLocalUrl = new URL(localUrl);
		let params: any = {}
		for (let p of newLocalUrl.searchParams) {
			params[p[0]] = p[1]
		}
		let redirectUrl = `/#/login?redirect=${newLocalUrl.pathname}`;
		if (Object.keys(params).length > 0) {
			redirectUrl += `&params=${JSON.stringify(params)}`
		} else  {
			redirectUrl += `&params={}`
		}
		return redirectUrl
	} catch (error) {
		console.log(error)
		return null
	}

}