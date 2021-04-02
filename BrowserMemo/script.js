let Data = {"URL": "", "TEXT": ""}

chrome.tabs.getSelected(tab=>{  // 現在のタブを取得
    text = String(tab.url)

    // URLパラメータを分解する
    if(text.indexOf("&") == -1){
        Data.URL = text;
    }else{
        Data.URL = text.split("&")[0];
    }
});

window.addEventListener('load',()=>{  // 拡張機能アイコンがクリックされて拡張機能ポップアップページが読み込まれたとき
    document.querySelector('#save-impression').addEventListener('click',()=>{
        Data.TEXT = document.querySelector("#textarea").value;
        var saveData = {[Data.URL]: [Data.TEXT]}

        chrome.storage.local.set(saveData, function(){
            console.log(saveData)
        });
    });
    document.querySelector('#load-impression').addEventListener('click',()=>{
        chrome.storage.local.get(Data.URL, function(value){
            document.querySelector("#last-impression").textContent = value[[Data.URL]]
            console.log(value[Data.URL])
        })

    });
})
