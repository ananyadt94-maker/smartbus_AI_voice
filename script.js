
const micButton = document.getElementById("micButton");
const speakButton = document.getElementById("speakButton");

const output = document.getElementById("output");
const response = document.getElementById("response");

let selectedLanguage = "en-IN";
let languageChosen = false;
let source = "";
let destination = "";
let journeyStep = "language";
function speakResponse() {
    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(response.innerText);
    speech.lang = selectedLanguage;
    speech.rate = 0.9;

    window.speechSynthesis.speak(speech);
}

function startListening() {
    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        output.innerText =
            "Speech recognition is not supported in this browser.";
        return;
    }

    const recognition = new SpeechRecognition();

    // First listen for the language choice in English.
    recognition.lang = languageChosen ? selectedLanguage : "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    output.innerText = "Listening...";

    recognition.onresult = function(event) {
        const userInput =
            event.results[0][0].transcript.trim();

        output.innerText = userInput;

        if (!languageChosen) {
            chooseLanguage(userInput);
        } else {
            processUserInput(userInput);
        }
    };

    recognition.onerror = function(event) {
        output.innerText = "Error: " + event.error;
    };

    recognition.start();
}
function chooseLanguage(text) {
    const choice = text.toLowerCase();

    if (choice.includes("kannada")) {
        selectedLanguage = "kn-IN";
    } else if (choice.includes("hindi")) {
        selectedLanguage = "hi-IN";
    } else if (choice.includes("english")) {
        selectedLanguage = "en-IN";
    } else {
        response.innerText = "Please say English, Kannada or Hindi.";
        speakThenListen();
        return;
    }

    languageChosen = true;
    journeyStep = "source";

    response.innerText = "Welcome! Where are you starting from?";
    speakThenListen();
}function processUserInput(text) {

    text = text.trim();

    // Don't accept empty voice input
    if (text === "") {
        response.innerText = "I didn't hear that. Please try again.";
        speakThenListen();
        return;
    }

    if (journeyStep === "source") {

        source = text;
        journeyStep = "destination";

        response.innerText =
            "Your starting point is " + source +
            ". Where do you want to go?";

        speakThenListen();
    }

    else if (journeyStep === "destination") {

        destination = text;
        journeyStep = "completed";

        output.innerText =
            "Starting point: " + source +
            " | Destination: " + destination;

        response.innerText =
            "Your journey is from " + source +
            " to " + destination +
            ". I am checking your journey.";

        speakResponse();
    }
}
function speakThenListen() {
    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(response.innerText);
    speech.lang = selectedLanguage;
    speech.rate = 0.9;

    speech.onend = function() {
        startListening();
    };

    window.speechSynthesis.speak(speech);
}

micButton.addEventListener("click", startListening);
speakButton.addEventListener("click", speakResponse);

// Initial welcome
response.innerText =
    "Welcome! Say English, Kannada or Hindi to choose your language.";

window.addEventListener("load", function() {
    speakResponse();
});
