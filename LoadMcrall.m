function M=LoadMcrall(fname)

M=[];

narginchk(1,1)
    

if ~exist(fname,'file')
    error([ fname ' DNE. Terminal'])
end


%% scan the header lines for forecast track, times, etc...
% import of data will happen below with "import data", much faster than fscaning the entire files
fid=fopen(fname,'r');

M.adv=fscanf(fid,'%s',1);
M.year=str2num(M.adv(5:end));
M.date=fscanf(fid,'%s',1);
M.month=str2num(M.date(1:2));
M.day=str2num(M.date(3:4));
M.hour=str2num(M.date(5:6));
M.date=datenum(M.year,M.month,M.day,M.hour,0,0);
M.name=fscanf(fid,'%s',1);
fscanf(fid,'%s',1);

M.tstart=fscanf(fid,'%f',1);  % hours, relative to "date" above
M.tend=fscanf(fid,'%f',1);
M.MonteCarloDt=fscanf(fid,'%f',1);
M.N=fscanf(fid,'%d',1);

c=0;
while true
    flag=fscanf(fid,'%s',1);
    if strcmp(flag(1),'t')
        break
    end
    c=c+1;
    M.Official_track.Time(c)=str2double(flag);
    M.Official_track.Lon(c)=fscanf(fid,'%f',1);
    M.Official_track.Lat(c)=fscanf(fid,'%f',1);
    M.Official_track.Intensity(c)=fscanf(fid,'%f',1);
    M.Official_track.GPCE(c)=fscanf(fid,'%f',1);
end
M.Official_track.Lon= M.Official_track.Lon-360;

M.ForecastTrackDt=M.Official_track.Time(end)/(c-1);  % forecast track dt
M.StepsPerTrack=(M.tend-M.tstart)/M.MonteCarloDt;
fclose(fid);

% bulk scan the file for the mc track data
A=importdata(fname,' ',c+2);
 
M.MC_Tracks.Vmax=reshape(A.data(:,2),M.StepsPerTrack+1,M.N);
M.MC_Tracks.Lat=reshape(A.data(:,3),M.StepsPerTrack+1,M.N);
M.MC_Tracks.Lon=reshape(A.data(:,4),M.StepsPerTrack+1,M.N)-360;
M.MC_Tracks.Rmax=reshape(A.data(:,5),M.StepsPerTrack+1,M.N);
M.MC_Tracks.RankineSize=reshape(A.data(:,6),M.StepsPerTrack+1,M.N);

M.MC_Tracks.R34=reshape(A.data(:,7:10),M.StepsPerTrack+1,M.N,4);
M.MC_Tracks.R50=reshape(A.data(:,11:14),M.StepsPerTrack+1,M.N,4);
M.MC_Tracks.R64=reshape(A.data(:,15:18),M.StepsPerTrack+1,M.N,4);
M.MC_Tracks.R100=reshape(A.data(:,19:22),M.StepsPerTrack+1,M.N,4);

M.MC_Tracks.ForwardSpeed=reshape(A.data(:,23),M.StepsPerTrack+1,M.N);
M.MC_Tracks.Beta=reshape(A.data(:,24),M.StepsPerTrack+1,M.N);
M.MC_Tracks.AsymmetryAmplitude=reshape(A.data(:,25),M.StepsPerTrack+1,M.N);
M.MC_Tracks.WindSpeedRotation=reshape(A.data(:,26),M.StepsPerTrack+1,M.N);


%% example plot, if ccplot is on the MATLAB path...
if exist('ccplot','file') && exist('plot_google_map','file')
    figure
    ccplot(M.MC_Tracks.Lon,M.MC_Tracks.Lat,M.MC_Tracks.Vmax,[0 140],'o',6,28);
    line(M.Official_track.Lon,M.Official_track.Lat,'LineWidth',3,'Color','c','Marker','o','LineStyle','-')
    drawnow
    axis('equal')
    axis([-90 -40 10 50])
    plot_google_map
    title(sprintf('%s : %s : N=%d',M.name,datestr(M.date),M.N))
    hcb=colorbar;
    colormap(jet(28))
    caxis([0 140])
    hcb.Label.String='Vmax Wind Speed [kt]';
    
    figure
    ccplot(M.MC_Tracks.Lon,M.MC_Tracks.Lat,M.MC_Tracks.Rmax,[0 60],'o',6,12);
    line(M.Official_track.Lon,M.Official_track.Lat,'LineWidth',3,'Color','c','Marker','o','LineStyle','-')
    drawnow
    axis('equal')
    axis([-90 -40 10 50])
    plot_google_map
    title(sprintf('%s : %s : N=%d',M.name,datestr(M.date),M.N))
    hcb=colorbar;
    colormap(jet(12))
    caxis([0 60])
    hcb.Label.String='Rmax [nmi]';
    
else
    disp('Neither ccplot nor plot_google_map functions could be found.  Can''t make example plot.')
end

