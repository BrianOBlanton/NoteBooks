test

%url='http://opendap.renci.org:1935/thredds/dodsC/Experiments/Isabel_ex1/ADCIRC/12km/n01/maxele.63.nc';
url='http://opendap.renci.org:1935/thredds/dodsC/daily/nam/2016030800/nc6b/hatteras.renci.org/dailyv51/namforecast/fort.63.nc';

which ncgeodataset

nc=ncgeodataset(url)

% get an ncgeovariable from the ncgeodataset nc
zeta=nc{'zeta'}                    % this does NOT extract the data from the nc file.
time=nc.time('time');              % get time variable in datenum format
%dtime=datetime(datevec(time));     % create a datetime object

% get the grid from the ncgeodataset object
fgs=ExtractGrid(nc);

% make a color surface plot fo the first time level
zeta1=zeta.data(1,:)';  % this DOES extract data, getting the first time level from the ncgeovariable
colormesh2d(fgs,zeta1)
axis('equal')
axis('tight')
colorbar
set(gca,'FontSize',6)
caxis([0 2])
colormap(parula(10))

% Compute strtree for grid
fgs.strtree=ComputeStrTree(fgs);


