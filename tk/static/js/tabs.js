function openTab(evt, links, tabs, tab) {
    links = document.querySelectorAll(links);
    tabs = document.querySelectorAll(tabs);
    tab = document.querySelector(tab);

    var i;
    for (i = 0; i < tabs.length; i++) {
        tabs[i].style.display = "none";
    }
    for (i = 0; i < links.length; i++) {
        links[i].className = links[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    tab.style.display = "block";
    if (evt) {
        evt.currentTarget.className += " active";
    }
}

function restoreOpenTab(links, tabs) {
    if (window.location.hash) {
        openTab(null, links, tabs, decodeURI(window.location.hash));
    }
}

function submitSearch(event) {
    event.preventDefault();

    fd = new FormData(event.originalTarget);
    var grouped = {};
    for (const e of fd) {
        if (!grouped[e[0]]) {
            grouped[e[0]] = [];
        }
        grouped[e[0]].push(e[1]);
    }

    var sp = new URLSearchParams();
    for (let key in grouped) {
        sp.set(key, grouped[key].join(","));
    }

    var url = new URL(event.target.action, window.location.href);
    url.search = "?" + decodeURIComponent(sp.toString());
    window.location.href = url.href;
};
