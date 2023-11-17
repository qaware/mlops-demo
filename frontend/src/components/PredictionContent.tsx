import * as React from 'react';
import {
    Button,
    Grid,
    Paper,
    Table, TableBody, TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Typography
} from "@mui/material";
import {predict} from "../service/BackendService";
import {useState} from "react";

export default function PredictionContent() {
    const [rows, setRows] = useState([["", ""]]);

    // Handle form submission
    const handleSubmit = async (event: React.ChangeEvent<any>) => {
        event.preventDefault(); // Prevent default form submission behavior

        try {
            const result = await predict(event.target[0].value.replace(/\s+/g, '').split(','));
            setRows(_ => { return result as string[][] }); // Update the state with the result
        } catch (error) {
            console.error('Error occurred:', error);
            // Handle error (e.g., update state to show error message)
        }
    };

    return (

        <Paper elevation={0} style={{margin: '2em', padding: '1em'}} variant='outlined'>
            <Typography variant="h4" component="div" sx={{flexGrow: 1}}>
                Prediction
            </Typography>
            <Grid container direction="row" marginTop={2} alignItems="flex-start">
                <Grid item xs={7} direction="row" rowSpacing={2}>
                    <form onSubmit={handleSubmit}>
                        <Grid item xs={12} style={{marginTop: '1em', marginBottom: '1em'}}>
                            <TextField id="label" label="word1, word2, word3" variant="outlined" fullWidth/>
                        </Grid>
                        <Grid item xs={12}>
                            <Button variant="contained" type="submit">
                                Predict
                            </Button>
                        </Grid>
                    </form>
                </Grid>
                <Grid item xs={4} direction="row" rowSpacing={2} marginLeft="auto">
                    <div id='predictionContent'>
                        <TableContainer component={Paper}>
                            <Table sx={{ minWidth: 300 }} aria-label="simple table">
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Good Words</TableCell>
                                        <TableCell>Bad Words</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody id="table">
                                    {rows.map((row) => (
                                        <TableRow>
                                            <TableCell id="gWords">{row[0]}</TableCell>
                                            <TableCell id="bWords">{row[1]}</TableCell>
                                        </TableRow>
                                        )
                                    )}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </div>
                </Grid>
            </Grid>
        </Paper>
    );
}
