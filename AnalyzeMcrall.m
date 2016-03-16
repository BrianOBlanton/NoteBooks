d='/Users/bblanton/Desktop/Dropbox';
files={
    'mcrall_al092011_082100.dat'
    'mcrall_al092011_082200.dat'
    'mcrall_al092011_082300.dat'
    'mcrall_al092011_082400.dat'
    'mcrall_al092011_082500.dat'
    'mcrall_al092011_082600.dat'
    'mcrall_al092011_082700.dat'
    'mcrall_al092011_082800.dat'
    };

for i=1:length(files)
    disp(files{i})
    M(i)=LoadMcrall([d '/' files{i}]);
end
