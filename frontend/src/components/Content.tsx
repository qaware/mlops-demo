import * as React from 'react';
import Container from '@mui/material/Container';
import { Box } from "@mui/material";
import TrainingContent from './TrainingContent';
import PredictionContent from './PredictionContent';

export default function Content() {
    return (

        <Container maxWidth="lg" style={{marginTop: '2em'}}>
            <Box>
                INSERT AN INITIAL EXPLAINING TEXT HERE
            </Box>
            <TrainingContent/>
            <PredictionContent/>

        </Container>
    );
}
