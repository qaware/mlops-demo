import * as React from 'react';
import { Button, Grid, Paper, TextField, Typography } from "@mui/material";

export default function TrainingContent() {
    return (

        <Paper elevation={0} style={{margin: '2em', padding: '1em'}} variant='outlined'>
            <Typography variant="h4" component="div" sx={{flexGrow: 1}}>
                Training
            </Typography>
            <Grid item xs={6}>
                <TextField id="label" label="Label" variant="outlined" fullWidth/>
            </Grid>
            <Grid item>
                <Button variant="contained">
                    Send new train data
                </Button>
            </Grid>
        </Paper>
    );
}
