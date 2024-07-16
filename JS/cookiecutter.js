



function getVar(key, obj) {
	var e = Error("The Requested value does not exist");
	try {
		retval = obj.get(key);
		if (retval == "" || retval == undefined || retval == null) {
			throw e;
		}
	} catch (err) {
		console.log(err)
		return null;

	}
	return retval;
}
var vars = document.cookie.split(";");
var __vars__ = new Map()
vars.forEach(element => {
	__vars__.set(element.split("=", 1)[0].trim(), element.split("=", 1)[1].trim());
	console.log("all variables set");
});

