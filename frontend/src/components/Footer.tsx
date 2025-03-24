import React from 'react';
import { Heart } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="w-full border-t bg-background/50 backdrop-blur-sm">
      <div className="max-w-screen-xl mx-auto px-4 py-4 flex flex-col items-center gap-2 text-sm text-muted-foreground">
        <p>No data of yours is being stored by the site!</p>
        <p className="flex items-center gap-1">
          Made with <Heart className="w-4 h-4 text-red-500 fill-current" /> by{' '}
          <a
            href="https://www.linkedin.com/in/sai-sashank-kuppa/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary hover:underline"
          >
            Sashank
          </a>
        </p>
      </div>
    </footer>
  );
};

export default Footer; 