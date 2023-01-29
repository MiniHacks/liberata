// Listen for messages
console.log("Parsing Site Info for Library Books.");

const URL = "http://localhost:8000";
// const URL = "https://project2023library-qwqi2iy3qa-uc.a.run.app";

window.onload = async (event) => {
  let data = { text: document.body.innerText, zipcode: "55414" };

  const common_fetch_params = {
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
    },
    redirect: "follow", // manual, *follow, error
    referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
  };

  let res = await fetch(`${URL}/get_only_titles`, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    body: JSON.stringify(data), // body data type must match "Content-Type" header,
    ...common_fetch_params
  });

  let respdata = await res.json();
  console.log(respdata)

  let recursive_find_replace = (node, find, parent = null) => {
    if (node.innerText?.toLowerCase().includes(find.toLowerCase()) || node.nodeValue?.toLowerCase().includes(find.toLowerCase())) {
      console.log(node)
      if (node.nodeType === Node.TEXT_NODE) {
        var text = node.nodeValue;

        let random_ass_id = "xxxxxxxxxxxxxxx".replace(/x/g, () => (Math.floor(Math.random() * 36)).toString(36));
        var boldText = `<span style='background-color: pink' id='${random_ass_id}'>${find}</span>`;
        var newHtml = text.toLowerCase().replace(find.toLowerCase(), boldText);
        var newNode = document.createElement('span');
        newNode.innerHTML = newHtml;
        parent.replaceChild(newNode, node);

        let show_modal_with_book_details = () => {
          // 1. Get the piece of text with the book name
          let textNode = document.getElementById(random_ass_id);

          // 2. When the modal is active, stop us from producing another one
          textNode.onmouseover = null;
          let bookTitle = find;

          // We precision place our modal to be right next to the text that the user moused over
          let { top, left, height, ...rest } = textNode.getBoundingClientRect();
          top += window.scrollY + height; // Y
          left += window.scrollX;


          // 3. Produce the modal
          console.log({ top, left, ...rest })
          const node = document.createElement("div");
          node.classList.add("card");
          node.setAttribute("style", `position: absolute; top: ${top}px; left: ${left}px; z-index: 100`);
          node.id = `${random_ass_id}-modal`;
          node.innerHTML = `
              <button class="delete" style="position: absolute; top: 0; right: 0; margin: 5px;" id="${random_ass_id}-deletebtn"></button>
              <div class="card-content">
                  <div class="media-content">
                    <p class="title is-4">${bookTitle}</p>
                    <p class="subtitle is-6" id="${random_ass_id}-authornames"><progress class="progress is-small" max="100">50%</progress></p>
                  </div>

                  <div class="content">
                    Available at the following libraries:
                    <ul id="${random_ass_id}-librarylist">
                      <progress class="progress is-small" max="100">50%</progress>
                    </ul>
                  </div>
              </div>
          `;

          // Show the modal in the DOM. We don't want it to inherit any funny styles -> make it a child of `body`
          document.body.appendChild(node);

          // 4. Make the modal delete button actually delete the modal
          document.getElementById(`${random_ass_id}-deletebtn`).onclick = function () {
            console.log("deleting ")
            document.body.removeChild(node);
            textNode.onmouseover = show_modal_with_book_details;
          };

          // 5. Make request to backend to get book details
          (async () => {
            let res = await fetch(`${URL}/book_details`, {
              method: "POST", // *GET, POST, PUT, DELETE, etc.
              body: JSON.stringify({
                book_title: bookTitle,
                zipcode: "55414"
              }), // body data type must match "Content-Type" header,
              ...common_fetch_params
            });
            let json = await res.json();

            let book = json[0];
            document.getElementById(`${random_ass_id}-authornames`).innerHTML = book.book_author;
            document.getElementById(`${random_ass_id}-librarylist`).innerHTML = book.available_at.map((library) => {
              let borrowhtml = '';
              if (library.link_to_borrow) {
                borrowhtml = `<a href="${library.link_to_borrow}"> Borrow :3 </a>`;
              }
              return `<li>${library.library_name} (${library.distance_str}) ${borrowhtml}</li>`;
            }).join("");
          }
          )();

        };
        document.getElementById(random_ass_id).onmouseover = show_modal_with_book_details;
      } else {

        for (const child of node.childNodes) {
          recursive_find_replace(child, find, node)
        }
      }
    }
  };

  for (const uwu of respdata) {
    // Get all elements in the document
    console.log(uwu)
    recursive_find_replace(document.body, uwu);
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
