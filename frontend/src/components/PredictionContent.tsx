import * as React from 'react';
import { Box, Button, Grid, Paper, TextField, Typography } from "@mui/material";

const handleSubmit = (event: React.ChangeEvent<any>) => {
    event.preventDefault();
    predict(event.target[0].value.replace(/\s+/g, '').split(','));
};

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

export default function PredictionContent() {
    return (

        <Paper elevation={0} style={{margin: '2em', padding: '1em'}} variant='outlined'>
            <form onSubmit={handleSubmit}>
            <Typography variant="h4" component="div" sx={{flexGrow: 1}}>
                Prediction
            </Typography>
            <Grid item xs={6}>
                <TextField id="label" label="word1, word2, word3" variant="outlined" fullWidth/>
            </Grid>
            <Grid item>
                <Button variant="contained" type="submit">
                    Predict
                </Button>
            </Grid>
            </form>
            <Box mt={5}>
                <Grid container justifyContent="flex-end">
                    <Button variant="contained" color="error">
                        Retrain
                    </Button>
                </Grid>
            </Box>
        </Paper>
    );
}
