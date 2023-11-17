import * as React from "react";
import {stopInterval} from "../App";

export async function getStatus() {
    await fetch('http://localhost:8080/status/', {
        method: 'GET',
    })
        .then((response) => response.text())
        .then((data) => {
            console.log(data)
            let progress = JSON.parse(data).progress as string
            document.getElementById('pipelineProgress')!.style.display = 'block';
            (document.getElementById('pipelineProgress')! as HTMLImageElement).src = `/pipeline_progress/${progress}.png`;
            if (progress == "verify_endpoint_done") {
                stopInterval();
                resetStatus();
            }
        })
        .catch((err) => {
            console.log(err.message);
        });
}

export async function resetStatus() {
    await fetch('http://localhost:8080/reset-status/', {
        method: 'GET',
    })
        .then((response) => response.text())
        .then((data) => {
            console.log(data)
        })
        .catch((err) => {
            console.log(err.message);
        });
}

export function triggerTraining(event: React.ChangeEvent<any>): Promise<void> {
    event.preventDefault();

    return runPipeline(event.target.goodWords.value.replace(/\s+/g, '').split(','),event.target.badWords.value.replace(/\s+/g, '').split(','));
}

const runPipeline = async (goodWords: string[], badWords: string[]) => {
    await fetch('http://localhost:8080/run/', {
        method: 'POST',
        body: JSON.stringify({
            good_words: goodWords,
            bad_words: badWords
        }),
        headers: {
            'Content-type': 'application/json',
        },
    })
        .then((response) => response.text())
        .then((data) => {
            if (data == 'OK') {
                document.getElementById('pipelineRun')!.innerText = 'Pipeline started!';
                // statusInterval();
            } else {
                document.getElementById('pipelineRun')!.innerText = 'Error while starting the pipeline!';
                console.log(data)
            }
        })
        .catch((err) => {
            console.log(err.message);
        });
};

export function triggerPrediction(event: React.ChangeEvent<any>): Promise<void> {
    event.preventDefault();
    return predict(event.target[0].value.replace(/\s+/g, '').split(','));
}

const predict = async (words: string[]) => {
    await fetch('http://localhost:8080/predict/', {
        method: 'POST',
        body: JSON.stringify({
            instances: words,
        }),
        headers: {
            'Content-type': 'application/json',
        },
    })
        .then((response) => response.text())
        .then((data) => {
            document.getElementById('predictionContent')!.hidden = false;
            document.getElementById('gWords')!.innerText = "";
            document.getElementById('bWords')!.innerText = "";
            let weight = JSON.parse(data);
            // alert(weight)
            words.reverse();
            for (const element in weight) {
                if (weight[element] == 'positive') {
                    if (document.getElementById('gWords')!.innerText.length > 0) {
                        document.getElementById('gWords')!.innerText = document.getElementById('gWords')!.innerText + ", ";
                    }
                    document.getElementById('gWords')!.innerText = document.getElementById('gWords')!.innerText+ words.pop() as string;
                } else if (weight[element] == 'negative') {
                    if (document.getElementById('bWords')!.innerText.length > 0) {
                        document.getElementById('bWords')!.innerText = document.getElementById('bWords')!.innerText + ", ";
                    }
                    document.getElementById('bWords')!.innerText = document.getElementById('bWords')!.innerText + words.pop() as string;
                } else {
                    alert('Unknown Error!')
                }
            }
        })
        .catch((err) => {
            console.log(err.message);
        });
};