'speechSynthesis' in window ? console.log("Web Speech API supported!") : console.log("Web Speech API not supported :-(")
const form = document.querySelector("#form")
const utterThis = new SpeechSynthesisUtterance()

const synth = window.speechSynthesis
const buttons = document.querySelectorAll("#submit-button")
const buttonsArray = Array.from(buttons);
let ourText = ""
const checkBrowserCompatibility = () => {
  "speechSynthesis" in window
    ? console.log("Web Speech API supported!")
    : console.log("Web Speech API not supported :-(")
}
checkBrowserCompatibility()

for (let i=0; i < buttonsArray.length ; i++) {
buttonsArray[i].addEventListener('click', (event) => {
    ourText = buttonsArray[i].role
    utterThis.text = ourText
    utterThis.lang = 'en-US';
    synth.speak(utterThis)
  });
}