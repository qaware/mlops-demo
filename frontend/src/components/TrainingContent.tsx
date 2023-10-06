import * as React from 'react';
import Container from '@mui/material/Container';
import { Box, Button, Grid, TextField } from "@mui/material";

export default function TrainingContent() {
    return (

        <Container style={{margin: '2em'}}>
            <Grid item xs={6}>
                <TextField id="label" label="Label" variant="outlined" fullWidth/>
            </Grid>
            <Grid item>
                <Button variant="contained">
                    Send new train data
                </Button>
            </Grid>
        </Container>
    );
}
