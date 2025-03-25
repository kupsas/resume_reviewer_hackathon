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
      <div className="max-w-screen-xl mx-auto flex items-center justify-between px-3 sm:px-4 py-2 sm:py-3">
        <Link to="/" className="flex items-center gap-2">
          <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-primary text-primary-foreground flex items-center justify-center">
            <FileText className="w-4 h-4 sm:w-5 sm:h-5" />
          </div>
          <span className="font-bold text-lg sm:text-xl">Resume Analyzer</span>
        </Link>
        
        <div className="flex items-center gap-2 sm:gap-3">
          <Button
            variant="outline"
            size="icon"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            className="rounded-full h-8 w-8 sm:h-10 sm:w-10"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? (
              <Sun className="h-4 w-4 sm:h-5 sm:w-5" />
            ) : (
              <Moon className="h-4 w-4 sm:h-5 sm:w-5" />
            )}
          </Button>
          
          {pathname === '/home' && (
            <Button asChild className="h-8 sm:h-10 text-sm sm:text-base">
              <Link to="/" className="flex items-center gap-1 sm:gap-2">
                <Upload className="w-3 h-3 sm:w-4 sm:h-4" />
                <span>Upload Resume</span>
              </Link>
            </Button>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
