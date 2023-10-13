import * as React from 'react';
import { Button, Grid, Paper, TextField, Typography } from "@mui/material";

const handleSubmit = (event: React.ChangeEvent<any>) => {
    event.preventDefault();
    runPipeline(event.target.goodWords.value.replace(/\s+/g, '').split(','),event.target.badWords.value.replace(/\s+/g, '').split(','));
};

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
            alert(data)
        })
        .catch((err) => {
            console.log(err.message);
        });
};

export default function TrainingContent() {
    return (

        <Paper elevation={0} style={{margin: '2em', padding: '1em'}} variant='outlined'>
            <form onSubmit={handleSubmit}>
            <Typography variant="h4" component="div" sx={{flexGrow: 1}}>
                Training
            </Typography>
            <Grid item xs={6}>
                <TextField id="goodWords" label="GoodWord1, GoodWord2, GoodWord3" variant="outlined" fullWidth/>
                <TextField id="badWords" label="BadWord1, BadWord2, BadWord3" variant="outlined" fullWidth/>
            </Grid>
            <Grid item>
                <Button variant="contained" type="submit">
                    Send new train data
                </Button>
            </Grid>
            </form>
        </Paper>
    );
}
