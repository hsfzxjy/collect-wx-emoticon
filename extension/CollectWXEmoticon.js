// ==UserScript==
// @name         CollectWxEmoticon
// @namespace    None
// @version      1.0.0
// @description  Automatically save emoticons in Web Wechat.
// @author       hsfzxjy
// @match        https://wx2.qq.com/*
// @grant        GM_download
// ==/UserScript==

function createButton() {
    const button = document.createElement('button')
    button.innerHTML = "Start Auto-saving Emotions"
    button.style = "position: fixed; right: 0; top: 0; font-size: .7em;"
    document.body.appendChild(button)

    const textMapping = {
        [false]: "Start Auto-saving Emotions",
        [true]: "Stop Auto-saving Emotions",
    }
    let started = false
    const updateText = () => { button.innerHTML = textMapping[started] }

    updateText()

    let callbacks = {
        [true]: () => {},
        [false]: () => {},
    }

    button.addEventListener("click", () => {
        started = !started
        updateText()
        callbacks[started]()
    })

    return {
        onStart(cb) { callbacks[true] = cb },
        onStop(cb) { callbacks[false] = cb },
    }
}

function saveImage(url, destDir) {
    const filename = btoa(url).replace('/', '+')
    GM_download({ url: url, name: destDir + '/' + filename, saveAs: false })
}

function handleChatMessage(el) {
    if (!el.classList.contains('emoticon')) return
    const url = el.querySelector('img').src
    saveImage(url, 'wx_emoticons')
}

function observerCallback(mutationsList) {
    for (const mutation of mutationsList) {
        if (mutation.type !== 'childList' || !mutation.addedNodes.length) continue
        handleChatMessage(mutation.addedNodes[0])
    }
}


function watchChatList() {
    const chatList = document.querySelector('[mm-repeat="message in chatContent"]')

    const mutationConfig = { childList: true, subtree: true }
    const observer = new MutationObserver(observerCallback)
    return {
        on: () => { observer.observe(chatList, mutationConfig) },
        off: () => { observer.disconnect() }
    }
}

(function() {
    'use strict';
    const button = createButton()
    const observer = watchChatList()
    button.onStart(() => observer.on())
    button.onStop(() => observer.off())
})();