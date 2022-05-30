import os
def main():
	import sys
	from .getOpts import opts
	from .funcs import StartExtract, UsageExtract, OrfFinder, GtfMaker, Reporter
	genome, gtf, pi, startCodon, outdir, prefix, pcov, nCores = opts()
	
	if not os.path.exists(outdir): os.makedirs(outdir)
	os.chdir(outdir)

	sys.stdout.write("OrfPP starts ..."+'\n')
	
	sys.stdout.write("\tPredicting preliminary ORFs"+'\n')
	OrfFinder(1, 'AUG', genome, gtf, pi, 0.001, nCores, 300, 'tmp')
	GtfMaker('tmp_orf.fa', 'tmp_sORF.gtf')
	
	sys.stdout.write("\tPredicting ORFs"+'\n')
	StartExtract(gtf, prefix)
	OrfFinder(0.5, startCodon, genome, gtf, pi, pcov, nCores, 60, prefix)
	Reporter(gtf, prefix+'.start.bed', prefix+'.stop.bed', prefix+'_orf.fa', prefix+'_ORF.gtf',prefix+'_orf_aa.fa', prefix+'_orf_table.txt', prefix+'_summary.txt')
	os.system('rm *.bed *tmp*')
	sys.stdout.write("OrfPP completed" + '\n')

if __name__ == "__main__":
	main()
