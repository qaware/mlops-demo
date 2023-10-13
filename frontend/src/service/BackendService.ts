import * as React from "react";

export function triggerTraining(event: React.ChangeEvent<any>): Promise<void> {
    event.preventDefault();
    return runPipeline(event.target.goodWords.value.replace(/\s+/g, '').split(','),event.target.badWords.value.replace(/\s+/g, '').split(','));; // TODO: call backend
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
                alert('Pipeline started!')
            } else {
                alert(data)
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
            alert(data)
        })
        .catch((err) => {
            console.log(err.message);
        });
};