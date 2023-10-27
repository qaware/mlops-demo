import * as React from 'react';
import {Box, Button, Grid, Paper, TextField, Typography} from "@mui/material";
import {triggerPrediction} from "../service/BackendService";

export default function PredictionContent() {
    return (

        <Paper elevation={0} style={{margin: '2em', padding: '1em'}} variant='outlined'>
            <form onSubmit={triggerPrediction}>
                <Typography variant="h4" component="div" sx={{flexGrow: 1}}>
                    Prediction
                </Typography>
                <Grid item xs={6} style={{marginTop: '1em', marginBottom: '1em'}}>
                    <TextField id="label" label="word1, word2, word3" variant="outlined" fullWidth/>
                </Grid>
                <Grid item xs={6}>
                    <Button variant="contained" type="submit">
                        Predict
                    </Button>
                </Grid>
            </form>
            <div id='predictionContent' hidden>
                <hr/>
                <Grid container rowSpacing={1} columnSpacing={{xs: 1, sm: 2, md: 3}}>
                    <Grid item xs={6}>
                        Good Words:
                        <Typography id="gWords" component="div" sx={{flexGrow: 1}}>
                            te
                        </Typography>
                    </Grid>
                    <Grid item xs={6}>
                        Bad Words:
                        <Typography id="bWords" component="div" sx={{flexGrow: 1}}>
                            st
                        </Typography>
                    </Grid>
                </Grid>
            </div>
        </Paper>
    );
}
