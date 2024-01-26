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

            setArrows(progress);

            if (progress == "deploy_done") {
                (document.getElementById('plot2')! as HTMLIFrameElement).contentWindow!.location.reload();
            }

            if (progress == "verify_endpoint_done") {
                stopInterval();
                resetStatus();
            }
        })
        .catch((err) => {
            console.log(err.message);
        });
}

function resetArrows() {
    document.getElementById("stepOneTitle")!.style.display = 'none';
    document.getElementById("stepTwoTitle")!.style.display = 'none';
    document.getElementById("stepThreeTitle")!.style.display = 'none';
    document.getElementById("stepFourTitle")!.style.display = 'none';
}

function setArrows(progress: string) {
    resetArrows();
    if (progress == "pipeline_started") {
        document.getElementById("stepOneTitle")!.style.display = 'block';
    }
    if (progress == "data_gen_done") {
        document.getElementById("stepTwoTitle")!.style.display = 'block';
    }
    if (progress == "train_done") {
        document.getElementById("stepThreeTitle")!.style.display = 'block';
    }
    if (progress == "deploy_done") {
        document.getElementById("stepFourTitle")!.style.display = 'block';
    }
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

    return runPipeline(event.target.goodWords.value.replace(/(?<=,|^)\s+|\s+(?=,|$)/g, '').split(','),event.target.badWords.value.replace(/(?<=,|^)\s+|\s+(?=,|$)/g, '').split(','));
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

export const predict = async (words: string[]) => {
    return fetch('http://localhost:8080/predict/', {
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
            const gW = [];
            const bW = [];

            let weight = JSON.parse(data);
            // alert(weight)
            words.reverse();
            for (const element in weight) {
                if (weight[element] == 'positive') {
                    gW.push(words.pop());
                } else if (weight[element] == 'negative') {
                    bW.push(words.pop());
                } else {
                    alert('Unknown Error!')
                }
            }
            let rows: string[][] = [];
            let size = gW.length > bW.length ? gW.length : bW.length;
            for (let i = 0; i < size; i++) {
                let good = gW.length > 0 ? gW.pop() as string : "";
                let bad = bW.length > 0 ? bW.pop() as string : "";

                rows.push([good, bad])
            }
            console.log(rows)

            return rows;
        })
        .catch((err) => {
            console.log(err.message);
        });
};