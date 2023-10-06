import * as React from 'react';
import Container from '@mui/material/Container';
import { Box, Button, Grid, TextField } from "@mui/material";

export default function PredictionContent() {
    return (

        <Container style={{margin: '2em'}}>
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
        </Container>
    );
}
