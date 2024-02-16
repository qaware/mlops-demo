import * as React from 'react';
import { AppBar, Box, Button, IconButton, Toolbar, Typography } from "@mui/material";

/**
 * Header element.
 */
export default function Header() {

    const blogPostUrl = 'https://blog.qaware.de/'
    const qawareUrl = 'https://qaware.de/'
    const githubUrl = 'https://github.com/qaware/mlops-demo'
    const openUrl = (url: string) => {
        window.open(url, '_blank');
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar>
                    <IconButton
                        size="large"
                        edge="start"
                        color="inherit"
                        aria-label="menu"
                        sx={{ mr: 2, p: 0, width: 128, height: 128 }}
                    >
                        <img src="/MLOps.png" alt="MLOps" style={{ maxHeight: '100%', maxWidth: '100%' }} />
                    </IconButton>
                    <Typography variant="h4" component="div" sx={{ flexGrow: 1 }}>
                        MLOps Demo Application
                    </Typography>
                    <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
                        <Button key='mlops-blog-post-button' sx={{ color: '#fff' }} onClick={() => openUrl(blogPostUrl)}>
                            MLOps Blog Post
                        </Button>
                        <Button key='qaware-button' sx={{ color: '#fff' }} onClick={() => openUrl(qawareUrl)}>
                            QAware
                        </Button>
                        <Button key='github-button' sx={{ color: '#fff' }} onClick={() => openUrl(githubUrl)}>
                            Github
                        </Button>
                    </Box>
                </Toolbar>
            </AppBar>
        </Box>
    );
}
