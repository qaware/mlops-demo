import {predict} from "../service/BackendService";
import {useState} from "react";
import {
    Button,
    Grid,
    Paper,
    Table, TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Typography
} from "@mui/material";
import * as React from "react";

export default function PredictionContent() {

    return (

        <Paper elevation={0} style={{margin: '2em', padding: '1em'}} variant='outlined'>
            <Typography variant="h4" component="div" sx={{flexGrow: 1}}>
                Plot
            </Typography>
            <Grid container direction="row" marginTop={2} alignItems="flex-start" spacing={2}>
                <Grid item xs={6} direction="row">
                    <Typography variant="body1" component="div">Existing Model</Typography>
                    <iframe src="http://127.0.0.1:8080/plot/" width={'100%'} height={400}/>
                </Grid>
                <Grid item xs={6} direction="row">
                    <Typography variant="body1" component="div">New Model</Typography>
                    <iframe id="plot2" src="http://127.0.0.1:8080/plot/" width={'100%'} height={400}/>
                </Grid>
            </Grid>
        </Paper>

    );
}