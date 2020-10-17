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
        var hash = decodeURI(window.location.hash).substr(1);
        openTab(null, links, tabs, "[id='" + hash + "']");
    }
}
