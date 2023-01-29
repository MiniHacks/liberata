// Listen for messages
console.log("Parsing Site Info for Library Books.");

window.onload = async (event) => {
  let data = { text: document.body.innerText };

  let res = await fetch("http://localhost:8000/extract_titles", {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: "follow", // manual, *follow, error
    referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data), // body data type must match "Content-Type" header
  });
  let respdata = await res.json();
  console.log(respdata)

  let recursive_find_replace = (node, find, parent = null) => {
    if (node.innerText?.includes(find) || node.nodeValue?.includes(find)) {
      console.log(node)
      if (node.nodeType === Node.TEXT_NODE) {
        var text = node.nodeValue;
        var boldText = `<span style='background-color: pink'>${find}</span>`;
        var newHtml = text.replace(find, boldText);
        var newNode = document.createElement('span');
        newNode.innerHTML = newHtml;
        parent.replaceChild(newNode, node);
      } else {

        for (const child of node.childNodes) {
          recursive_find_replace(child, find, node)
        }
      }
    }
  };

  for (const uwu in respdata) {
    if (respdata.hasOwnProperty(uwu)) {
      // Get all elements in the document
      recursive_find_replace(document.body, uwu);
    }
  }

  if (respdata != null) {
    const overlay = document.createElement("button");
    overlay.setAttribute('onclick', 'alert("button")')
    overlay.setAttribute('type', 'button')
    const fill = document.createElement("div")
    fill.setAttribute('id', 'overlay')
    // overlay.id = "overlay"
    // let c = "position: fixed; margin: auto; z-index: 999; width: 50px; height: 50px; -webkit - border - radius: 25px; -moz - border - radius: 25px; border - radius: 25px; background: blue; foreground: red"
    // let c = "background: #fff; position: fixed; top: 0; left: 0; width: 100%; z-index: 999px; box-shadow: 0px 0px 6px 0px";  // rgba(0, 0, 0, 0.5);"

    // overlay.setAttribute('style', c)

    const body = document.querySelector('body');
    body.insertBefore(overlay, body.children[0])
    overlay.appendChild(fill)
    // body.insertAdjacentElement("afterend", overlay);
  }
};
