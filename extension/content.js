// Listen for messages
console.log("Parsing Site Info for Library Books.");

const URL = "http://localhost:8000";
// const URL = "https://project2023library-qwqi2iy3qa-uc.a.run.app";

window.onload = async (event) => {
  let zipcode = await chrome.storage.sync.get(["zipcode"]);
  if (zipcode == null) {
    zipcode = "55414";
  } else {
    zipcode = zipcode.zipcode;
  }
  let data = { text: document.body.innerText, zipcode };

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

  const checkstroverlap = (str1, str2) => {
    if (!str1 || !str2) return 0;

    for (let str2_offsetfromstr1 = 0; str2_offsetfromstr1 < str1.length; str2_offsetfromstr1++) {
      let str1_sub = str1.substring(str2_offsetfromstr1, str2_offsetfromstr1 + str2.length);
      let str2_sub = str2.substring(0, str1.length - str2_offsetfromstr1)
      if (str1_sub == str2_sub) {
        return true;
      }
    }
    return false;
  }

  let recursive_find_replace = (node, find, parent = null) => {
    const forwardoverlap = checkstroverlap(find.og_text.toLowerCase().trim(), (node.innerText || node.nodeValue)?.toLowerCase()?.trim());
    const backwardoverlap = checkstroverlap((node.innerText || node.nodeValue)?.toLowerCase()?.trim(), find.og_text.toLowerCase().trim());


    let show_modal_with_book_details = (random_ass_id) => () => {
      // 1. Get the piece of text with the book name
      let textNode = document.getElementById(random_ass_id);

      // 2. When the modal is active, stop us from producing another one
      textNode.onmouseover = null;
      let bookTitle = find.title;

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
                <p class="subtitle is-6" id="${random_ass_id}-authornames">${find.author || '<progress class="progress is-small" max="100">50%</progress>'}</p>
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
        textNode.onmouseover = show_modal_with_book_details(random_ass_id);
      };

      // 5. Make request to backend to get book details
      (async () => {
        let res = await fetch(`${URL}/book_details`, {
          method: "POST", // *GET, POST, PUT, DELETE, etc.
          body: JSON.stringify({
            book_title: bookTitle,
            zipcode
          }), // body data type must match "Content-Type" header,
          ...common_fetch_params
        });
        let json = await res.json();

        let book = json[0];
        document.getElementById(`${random_ass_id}-authornames`).innerHTML = book.book_author;
        document.getElementById(`${random_ass_id}-librarylist`).innerHTML = book.available_at.map((library) => {
          let borrowhtml = '';
          if (library.link_to_borrow) {
            borrowhtml = `<a href="${library.link_to_borrow}" target="_blank" rel="noopener noreferrer" style="all: initial; color: blue"> Borrow :3 </a>`;
          }
          return `<li>${library.library_name} (${library.distance_str}) ${borrowhtml}</li>`;
        }).join("");
      }
      )();

    };

    let random_ass_id = "xxxxxxxxxxxxxxx".replace(/x/g, () => (Math.floor(Math.random() * 36)).toString(36));
  
    if (node.innerText?.toLowerCase().includes(find.og_text.toLowerCase()) || node.nodeValue?.toLowerCase().includes(find.og_text.toLowerCase())
    ) {
      if (node.nodeType === Node.TEXT_NODE) {
        let bigger_overlap = Math.max(forwardoverlap, backwardoverlap);
        let is_forwards = bigger_overlap === forwardoverlap; // forwards means that og text is to left of node text
        // backwards means that node text is left of og text
        let nodeText = node.nodeValue;
        let boldText = `<span style='background-color: pink' id='${random_ass_id}'>${find.og_text}</span>`;
        let newHtml = nodeText.toLowerCase().replace(find.og_text.toLowerCase(), boldText);
        if (newHtml == nodeText.toLowerCase()) {

          let front = is_forwards ? "" : nodeText;
          let back = is_forwards ? nodeText : "";

          // last overlap letters of front == first overlap letters of back

          let to_highlight = back.substring(0, bigger_overlap);

          let boldText = `${front.substring(0, front.length - bigger_overlap)}<span style='background-color: pink' id='${random_ass_id}'>${to_highlight}</span>${back.substring(bigger_overlap)}`;
          newHtml = boldText;
        }
        let newNode = document.createElement('span');
        newNode.innerHTML = newHtml;
        parent.replaceChild(newNode, node);

        setTimeout(() => document.getElementById(random_ass_id).onmouseover = show_modal_with_book_details(random_ass_id), 500)
        return true;
      } else {
        let any_contain_it = [...node.childNodes].map((x) => recursive_find_replace(x, find, node)).some((x) => !!x);
        if (!any_contain_it) {
          node.style['background-color'] = "pink";
          node.id = random_ass_id;
          node.onmouseover = show_modal_with_book_details(random_ass_id)
        }
        return true;
      }
    }
    return false;
  };

  for (const uwu of respdata) {
    // Get all elements in the document
    console.log(uwu)
    recursive_find_replace(document.body, uwu);
  }
};
