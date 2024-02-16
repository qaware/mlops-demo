import * as React from 'react';
import { Box, Paper, Typography } from "@mui/material";
import Container from '@mui/material/Container';

/**
 * Footer element.
 */
export default function Footer() {
    return (
        <Paper sx={{
            marginTop: 'calc(2%)',
            width: '100%',
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
                    <Typography variant="body1" color="initial">
                        © 2024 QAware Gmbh
                    </Typography>
                </Box>
            </Container>
        </Paper>
    );
}
