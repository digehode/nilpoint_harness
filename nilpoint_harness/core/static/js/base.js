//biome-ignore lint/correctness/noUnusedVariables: used in template
function toggle_dark() {
    if (themeSwitcher.scheme === "light") {
        console.log("Scheme is currently light, setting to dark");
        themeSwitcher.scheme = "dark";
    } else {
        console.log("Scheme is currently not light, setting to light");
        themeSwitcher.scheme = "light";
    }
}
