function colorToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(color) {
    const c = color.split(','),
          r = parseInt(c[0].slice(4)),
          g = parseInt(c[1]),
          b = parseInt(c[2])
    return "#" + colorToHex(r) + colorToHex(g) + colorToHex(b);
}

function ColorLuminance(color, percent) {
    let f = color.split(','),
        t = percent < 0 ? 0 : 255,
        p = percent < 0 ? percent *-1 : percent,
        R = parseInt(f[0].slice(4)),
        G = parseInt(f[1]),
        B = parseInt(f[2]);
    let r = Math.round((t - R) * p) + R,
        g = Math.round((t - G) * p) + G,
        b = Math.round((t - B) * p) + B
    return `rgb(${r}, ${g}, ${b})`;
}

const colors = document.querySelectorAll('.palette-color')

function addShades(e) {
    const baseColor = e.style.backgroundColor
    let shades = []
    for (let i = 1; i >= -1; i -= 0.5) {
        let shade = ColorLuminance(baseColor, i)
        shades.push(shade)
    }
    let shadeButtons = ""
    shades.forEach(shade => {
        shadeButtons += `<div class="shade" style="background-color: ${shade}"></div>`
    })

    e.innerHTML += '<div class="color-shades">' + shadeButtons + '</div>'
}

colors.forEach(color => {
    addShades(color)
})
