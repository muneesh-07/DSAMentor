// src/components/Navbar.jsx - Non-fixed version
import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Code,
  GitHub,
  LightMode,
  Psychology,
  Analytics,
  Speed,
} from '@mui/icons-material';

const Navbar = () => {
  return (
    <AppBar 
      position="static"  // Changed from "fixed" to "static"
      sx={{ 
        backgroundColor: 'rgba(245, 245, 240, 0.95)',
        backdropFilter: 'blur(10px)',
        color: 'text.primary',
        boxShadow: '0 2px 20px rgba(93, 134, 108, 0.1)',
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        {/* Logo and Title */}
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Box
            sx={{
              width: 40,
              height: 40,
              backgroundColor: 'primary.main',
              borderRadius: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mr: 2,
            }}
          >
            <Psychology sx={{ color: 'white', fontSize: 24 }} />
          </Box>
          <Typography
            variant="h5"
            component="div"
            sx={{
              fontWeight: 700,
              background: 'linear-gradient(135deg, #5D866C, #C2A68C)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            DSA Mentor
          </Typography>
        </Box>

        {/* Feature Indicators */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            backgroundColor: 'primary.light',
            px: 2,
            py: 1,
            borderRadius: 3,
            gap: 1
          }}>
            <Analytics sx={{ fontSize: 20, color: 'white' }} />
            <Typography variant="body2" sx={{ color: 'white', fontWeight: 600 }}>
              3-in-1 AI Analysis
            </Typography>
          </Box>

          {/* GitHub Link */}
          <Tooltip title="View on GitHub">
            <IconButton
              component="a"
              href="https://github.com/muneesh07/dsa-mentor"
              target="_blank"
              rel="noopener noreferrer"
              sx={{ 
                color: 'text.primary',
                '&:hover': { 
                  backgroundColor: 'primary.main',
                  color: 'white'
                }
              }}
            >
              <GitHub />
            </IconButton>
          </Tooltip>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
