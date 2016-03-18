function structfields2mat(s,matname)

flds=fieldnames(s);

for i=1:length(flds)

  com=sprintf('%s=s.%s;',flds{i},flds{i});
  eval(com)
end

sflds=strjoin(flds,''',''');
sflds=sprintf('''%s''',sflds);
whos

save(matname,sflds,'-v7.3')
