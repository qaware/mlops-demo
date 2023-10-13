import * as React from 'react';
import { Box, Button, Grid, Paper, TextField, Typography } from "@mui/material";
import {triggerPrediction} from "../service/BackendService";

export default function PredictionContent() {
    return (

        <Paper elevation={0} style={{margin: '2em', padding: '1em'}} variant='outlined'>
            <form onSubmit={triggerPrediction}>
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
