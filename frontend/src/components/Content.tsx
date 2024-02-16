import * as React from 'react';
import Container from '@mui/material/Container';
import {Box, Typography} from "@mui/material";
import TrainingContent from './TrainingContent';
import PredictionContent from './PredictionContent';
import DocumentationContent from './DocumentationContent';
import PlotContent from './PlotContent';

export default function Content() {
    return (

        <Container maxWidth="lg" style={{marginTop: '2em'}}>
            <Box>
                <Typography variant="subtitle1" component="div" sx={{ flexGrow: 1 }}>
                    In the following the MLOps use case of fast and efficient incorporation of production data will be explored.
                    You will see how an already deployed model can be seamlessly re-trained, re-evaluated, and re-deployed fully automatically.
                    Furthermore you can explore how the model changes its decision boundary based on your newly entered training data.
                </Typography>
            </Box>
            <TrainingContent/>
            <PlotContent/>
            <PredictionContent/>
            <DocumentationContent/>
        </Container>
    );
}
