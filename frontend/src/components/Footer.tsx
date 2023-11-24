import * as React from 'react';
import { Box, Paper, Typography } from "@mui/material";
import Container from '@mui/material/Container';

/**
 * Footer element.
 */
export default function Footer() {
    return (
        <Paper sx={{
            marginTop: 'calc(10% + 60px)',
            width: '100%',
            position: 'fixed',
            bottom: 0,
            zIndex: 5,
        }} component="footer" square variant="outlined">
            <Container maxWidth="lg">
                <Box
                    sx={{
                        flexGrow: 1,
                        justifyContent: "center",
                        display: "flex",
                        my: 1
                    }}
                >
                </Box>

                <Box
                    sx={{
                        flexGrow: 1,
                        justifyContent: "center",
                        display: "flex",
                        mb: 2,
                    }}
                >
                    <Typography variant="caption" color="initial">
                        TODO FOOTER
                    </Typography>
                </Box>
            </Container>
        </Paper>
    );
}
