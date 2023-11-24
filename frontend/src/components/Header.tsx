import * as React from 'react';
import { AppBar, Box, Button, IconButton, Toolbar, Typography } from "@mui/material";

/**
 * Header element.
 */
export default function Header() {
    return (
        <Box sx={{flexGrow: 1}}>
            <AppBar position="static">
                <Toolbar>
                    <IconButton
                        size="large"
                        edge="start"
                        color="inherit"
                        aria-label="menu"
                        sx={{mr: 2}}
                    >
                    </IconButton>
                    <Typography variant="h4" component="div" sx={{flexGrow: 1}}>
                        MLOps Demo Application
                    </Typography>
                    <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
                        <Button key='mlops-documentation-button' sx={{ color: '#fff' }}>
                            MLOps Doku
                        </Button>
                        <Button key='mlops-documentation-button' sx={{ color: '#fff' }}>
                            QAware
                        </Button>
                        <Button key='mlops-documentation-button' sx={{ color: '#fff' }}>
                            Github
                        </Button>
                    </Box>
                </Toolbar>
            </AppBar>
        </Box>
    );
}
