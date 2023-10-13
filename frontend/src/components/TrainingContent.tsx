import * as React from 'react';
import { Button, Grid, Paper, TextField, Typography } from "@mui/material";
import {triggerTraining} from "../service/BackendService";


export default function TrainingContent() {
    return (

        <Paper elevation={0} style={{margin: '2em', padding: '1em'}} variant='outlined'>
            <form onSubmit={triggerTraining}>
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
