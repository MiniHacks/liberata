window.addEventListener("load", function () {
  const elem = document.getElementById("switch");
  const zipper = document.getElementById("zipper");
  let active = true;
  chrome.storage.sync.get(["zipcode"]).then((result) => {
    console.log(result.zipcode);
    active = result.zipcode ? false : true;
    if (!active) {
      elem.classList.remove("is-success");
      elem.classList.add("is-danger");
      elem.innerText = "No";
      zipper.value = result.zipcode;
    } else {
      elem.classList.remove("is-danger");
      elem.classList.add("is-success");
      elem.innerText = "Yes";
    }
    zipper.disabled = active;
  });
  elem.onclick = () => {
    if (active) {
      elem.classList.remove("is-success");
      elem.classList.add("is-danger");
      elem.innerText = "No";
    } else {
      elem.classList.remove("is-danger");
      elem.classList.add("is-success");
      elem.innerText = "Yes";
      zipper.value = "";
      chrome.storage.sync.set({ "zipcode": "" });
    }
    active = !active;
    zipper.disabled = active;
  };
  zipper.onchange = () => {
    chrome.storage.sync.set({ "zipcode": zipper.value });
  }
});
