import Image from 'next/image';

const Header = () => {
  return (
    <header className="bg-gray-800 border-b border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <Image src="/file.svg" alt="Logo" width={32} height={32} className="w-8 h-8" />
            </div>
            <h1 className="text-xl font-semibold text-white">Resume Reviewer AI</h1>
          </div>
          <nav className="flex space-x-4">
            <a
              href="https://github.com/kupsas/resume_reviewer_hackathon"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-300 hover:text-white transition-colors"
            >
              GitHub
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 