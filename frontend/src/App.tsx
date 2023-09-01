import * as React from 'react';
import Container from '@mui/material/Container';
import {Box, Button, Grid, TextField} from "@mui/material";

export default function App() {
    return (
        <Container maxWidth="lg">
            <Grid container spacing={1}>
                <Grid item xs={6}>
                    <TextField id="word" label="Word" variant="outlined" fullWidth />
                </Grid>
                <Grid item xs={6}>
                    <TextField id="label" label="Label" variant="outlined" fullWidth />
                </Grid>
            </Grid>
            <Box mt={3}>
                <Grid container spacing={3} justifyContent="flex-end">
                    <Grid item xs={5}>
                        <Button variant="contained">
                            Predict
                        </Button>
                    </Grid>
                    <Grid item>
                        <Button variant="contained">
                            Send new train data
                        </Button>
                    </Grid>
                </Grid>
            </Box>
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
