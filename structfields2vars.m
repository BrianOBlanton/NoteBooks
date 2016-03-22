function structfields2vars(s,matname)

save(matname,'-v7.3','-struct','s')

if isfield(s,'TheGrid')
    TheGrid=s.TheGrid;
    save(matname,'-v7.3','-struct','TheGrid','-append')
end

return


flds=fieldnames(s);

for i=1:length(flds)
  com=sprintf('%s=s.%s;',flds{i},flds{i});
  eval(com)
end

% if isfield(s,'TheGrid')
%     com=sprintf('%s=s.%s;','elements','TheGrid.e');
%     eval(com)
%     flds{end+1}='elements';
%     com=sprintf('%s=s.%s;','lon','TheGrid.x');
%     eval(com)
%     flds{end+1}='lon';
%     com=sprintf('%s=s.%s;','lat','TheGrid.y');
%     eval(com)
%     flds{end+1}='lat';
% end

sflds=strjoin(flds,''',''');
sflds=sprintf('''%s''',sflds);
%whos

save(matname,'-v7.3',sflds)
