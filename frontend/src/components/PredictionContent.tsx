import * as React from 'react';
import { Box, Button, Grid, Paper, TextField, Typography } from "@mui/material";

export default function PredictionContent() {
    return (

        <Paper elevation={0} style={{margin: '2em', padding: '1em'}} variant='outlined'>
            <Typography variant="h4" component="div" sx={{flexGrow: 1}}>
                Prediction
            </Typography>
            <Grid item xs={6}>
                <TextField id="label" label="Label" variant="outlined" fullWidth/>
            </Grid>
            <Grid item>
                <Button variant="contained">
                    Predict
                </Button>
            </Grid>
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
