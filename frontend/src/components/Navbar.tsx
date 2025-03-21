import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FileText, Upload, Sun, Moon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTheme } from '@/components/ThemeProvider';

const Navbar = () => {
  const { pathname } = useLocation();
  const { theme, setTheme } = useTheme();

  return (
    <header className="border-b bg-gradient-to-r from-background to-secondary/30">
      <div className="max-w-screen-xl mx-auto flex items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-lg bg-primary text-primary-foreground flex items-center justify-center">
            <FileText className="w-5 h-5" />
          </div>
          <span className="font-bold text-xl">Resume Analyzer</span>
        </Link>
        
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="icon"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            className="rounded-full"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? (
              <Sun className="h-5 w-5" />
            ) : (
              <Moon className="h-5 w-5" />
            )}
          </Button>
          
          {pathname === '/home' && (
            <Button asChild>
              <Link to="/" className="flex items-center gap-2">
                <Upload className="w-4 h-4" />
                <span>Upload Resume</span>
              </Link>
            </Button>
          )}
          
          {pathname === '/' && (
            <Button variant="outline" asChild>
              <Link to="/home" className="flex items-center gap-2">
                <span>View Analysis</span>
              </Link>
            </Button>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
