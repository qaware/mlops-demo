import * as React from 'react';
import { Button, Grid, Paper, TextField, Typography } from "@mui/material";
import { triggerTraining } from "../service/BackendService";

export default function TrainingContent() {
    return (

        <Paper elevation={0} style={{margin: '2em', padding: '1em'}} variant='outlined'>
            <form onSubmit={triggerTraining}>
                <Typography variant="h4" component="div" sx={{flexGrow: 1}}>
                    Training
                </Typography>
                <Grid container direction="row" marginTop={2} alignItems="flex-start">
                    <Grid container xs={8} direction="row" rowSpacing={2}>
                        <Grid item xs={13}>
                            <TextField id="goodWords" label="Good Sentence 1, Good Sentence 2, Good Sentence 3" variant="outlined"
                                       fullWidth/>
                        </Grid>
                        <Grid item xs={13}>
                            <TextField id="badWords" label="Bad Sentence 1, Bad Sentence 2, Bad Sentence 3" variant="outlined" fullWidth/>
                        </Grid>
                        <Grid item xs={13} >
                            <Grid container justifyContent="flex-end">
                                <Typography id="pipelineRun" component="div" sx={{flexGrow: 1}} style={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    height: '100%'
                                }}/>
                                <Button variant="contained" type="submit">
                                    Send new train data
                                </Button>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item xs={3} marginLeft="auto" >
                        <Grid container rowSpacing={1} height={450} columnSpacing={{xs: 1, sm: 2, md: 3}} sx={{ backgroundColor: 'lightgray' }}>
                                <img id="pipelineProgress" alt="pipeline progress" src="/pipeline_progress/reset.png"
                                     style={{display: 'block', marginLeft: 'auto', marginRight: 'auto', width: '100%'}}/>
                        </Grid>

                    </Grid>
                </Grid>

            </form>

        </Paper>
    );
}
