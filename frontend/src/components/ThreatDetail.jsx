import { useState } from 'react'
import { useUpdateStatus } from '../hooks/useThreats'
import client from '../api/client'

const SEV_LABEL = { CRITICAL: 'KRITIS', HIGH: 'TINGGI', MEDIUM: 'SEDANG', LOW: 'RENDAH' }
const SEV_VAR = {
  CRITICAL: { bg: '--sev-kritis-bg', color: '--sev-kritis-text', border: '--sev-kritis-bdr' },
  HIGH: { bg: '--sev-tinggi-bg', color: '--sev-tinggi-text', border: '--sev-tinggi-bdr' },
  MEDIUM: { bg: '--sev-sedang-bg', color: '--sev-sedang-text', border: '--sev-sedang-bdr' },
  LOW: { bg: '--sev-rendah-bg', color: '--sev-rendah-text', border: '--sev-rendah-bdr' },
}
const STATUS_LABEL = { NEW: 'Baru', VERIFIED: 'Terverifikasi', MITIGATED: 'Dimitigasi', FALSE_POSITIVE: 'Positif Palsu' }
const SRC_LABEL = { TELEGRAM: 'Telegram', PASTE: 'Paste Site', GITHUB: 'GitHub', HIBP: 'HIBP', GOOGLE_DORK: 'Google Dork' }
const ENTITY_LABEL = { CREDIT_CARD: 'Kartu Kredit', NIK: 'NIK', NPWP: 'NPWP', CREDENTIAL: 'Kredensial', ACCOUNT_NUMBER: 'No. Rekening', CVV: 'CVV', BANK_NAME: 'Nama Bank', BANKING_KEYWORD: 'Keyword' }
const ENTITY_PLAIN = { CREDIT_CARD: 'nomor kartu kredit', NIK: 'Nomor Induk Kependudukan (NIK)', NPWP: 'Nomor Pokok Wajib Pajak (NPWP)', CREDENTIAL: 'kredensial akses', ACCOUNT_NUMBER: 'nomor rekening bank', CVV: 'kode keamanan kartu' }
const REKOMENDASI = {
  CREDIT_CARD: 'Koordinasi dengan issuer untuk blokir batch kartu terdampak. Notifikasi nasabah via SMS/email.',
  NIK: 'Laporkan ke Dukcapil. Monitor penggunaan NIK di layanan onboarding.',
  CREDENTIAL: 'Force password reset akun terdampak. Aktifkan 2FA wajib.',
  CVV: 'Aktifkan 3D Secure untuk transaksi online. Tingkatkan monitoring transaksi CNP.',
  NPWP: 'Koordinasi dengan DJP. Pantau aktivitas perpajakan mencurigakan.',
  ACCOUNT_NUMBER: 'Tingkatkan monitoring transaksi pada rekening terekspos. Hubungi nasabah.',
}

function maskValue(val, type) {
  if (!val) return '-'
  if (type === 'CREDIT_CARD') { const d = val.replace(/[^0-9\u2022*X]/g, ''); if (d.length >= 8) return `${val.slice(0,4)} \u2022\u2022\u2022\u2022 \u2022\u2022\u2022\u2022 ${val.slice(-4)}` }
  if (type === 'NIK' && val.length >= 10) return `${val.slice(0,6)} \u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022 ${val.slice(-2)}`
  if (type === 'CREDENTIAL' && val.includes('@')) { const at = val.indexOf('@'), dot = val.lastIndexOf('.'); if (at > 2 && dot > at) return `${val.slice(0,3)}\u2022\u2022\u2022@\u2022\u2022\u2022\u2022${val.slice(dot)}` }
  if (val.length <= 8) return val; return val.slice(0,4)+'\u2022'.repeat(Math.max(val.length-8,4))+val.slice(-4)
}
function formatDate(iso) { return new Date(iso).toLocaleString('id-ID', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }) }
function formatDateWib(iso) {
  const d = new Date(iso), wib = new Date(d.getTime()+(7*60+d.getTimezoneOffset())*60000)
  const bulan = ['','Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember']
  return `${String(wib.getDate()).padStart(2,'0')} ${bulan[wib.getMonth()+1]} ${wib.getFullYear()}, ${String(wib.getHours()).padStart(2,'0')}:${String(wib.getMinutes()).padStart(2,'0')} WIB`
}
function sensitiveTypes(entities) { return [...new Set(entities.map(e=>e.type).filter(t=>!['BANK_NAME','BANKING_KEYWORD'].includes(t)))] }
function entityTypesPlain(entities) { return sensitiveTypes(entities).map(t=>ENTITY_PLAIN[t]||ENTITY_LABEL[t]||t).join(', ')||'data keuangan' }

function generateNotifikasiOJK(t) {
  const entities=t.detected_entities?.entities||[], tags=(t.institution_tags||[]).join(', ')||'[ISI NAMA BANK]', src=SRC_LABEL[t.source_type]||t.source_type, dp=entityTypesPlain(entities)
  const reks=sensitiveTypes(entities).filter(k=>REKOMENDASI[k]).slice(0,3).map((k,i)=>`   ${i+1}. ${REKOMENDASI[k]}`); while(reks.length<3)reks.push(`   ${reks.length+1}. [ISI LANGKAH MITIGASI]`)
  const ec={}; entities.forEach(e=>{ec[e.type]=(ec[e.type]||0)+1}); const tbl=Object.entries(ec).sort().map(([t,c])=>`   ${(ENTITY_LABEL[t]||t).padEnd(35)} ${String(c).padStart(8)}`).join('\n')
  return ['\u2501'.repeat(45),'DRAFT NOTIFIKASI AWAL INSIDEN SIBER','[BELUM RESMI \u2014 Perlu ditinjau dan ditandatangani pejabat berwenang',' sebelum disampaikan ke OJK]','Mengacu: SEOJK No. 29/SEOJK.03/2022 Bab IX huruf (a)',`Nomor Draft    : DRAFT-NSFI-${(t.id||'').slice(0,8).toUpperCase()}`,'Dibuat oleh    : NusaShield FI Monitoring Platform',`Tanggal draft  : ${formatDateWib(t.created_at)}`,'\u2501'.repeat(45),'','A. IDENTITAS BANK PELAPOR','   Nama Bank         : [ISI NAMA BANK]','   Kode Bank         : [ISI KODE BANK]','   Nama Penanggung   : [ISI NAMA PEJABAT]','   Jabatan           : [ISI JABATAN]','   Kontak            : [ISI EMAIL/TELEPON]','','B. INFORMASI INSIDEN','   Tanggal/Waktu insiden pertama terdeteksi oleh NusaShield FI:',`     ${formatDateWib(t.created_at)}`,'',`   Sumber deteksi    : ${src}`,`   URL sumber        : ${t.source_url||'-'}`,`   Risk score        : ${t.risk_score}/100 (${SEV_LABEL[t.severity]||t.severity})`,'','   Deskripsi singkat insiden:',`   Ditemukan indikasi kebocoran data ${dp}`,`   nasabah ${tags} sebanyak estimasi ${entities.length} entitas`,`   yang dipublikasikan di ${src}.`,`   Data yang terekspos meliputi ${dp}.`,'','C. ESTIMASI DAMPAK AWAL',`   Jenis data terekspos  : ${dp}`,`   ${'Tipe Data'.padEnd(35)} ${'Jumlah'.padStart(8)}`,`   ${'-'.repeat(45)}`,tbl,`   ${'-'.repeat(45)}`,`   ${'TOTAL'.padEnd(35)} ${String(entities.length).padStart(8)}`,`   Lembaga terdampak     : ${tags}`,'','   CATATAN: Estimasi ini bersumber dari deteksi otomatis NusaShield FI','   dan PERLU DIVERIFIKASI oleh tim keamanan internal sebelum','   dicantumkan dalam laporan resmi.','','D. LANGKAH MITIGASI AWAL','   [Isi sesuai tindakan yang telah diambil oleh bank]','','   Rekomendasi NusaShield FI berdasarkan tipe data:',...reks,'','E. STATUS PELAPORAN',`   Status saat ini   : ${STATUS_LABEL[t.status]||t.status}`,'   Diverifikasi oleh : [ISI NAMA ANALIS]','   Tanggal verifikasi: [ISI TANGGAL]','','\u2501'.repeat(45),'DOKUMEN BERIKUTNYA YANG DIPERLUKAN:','Laporan Insiden Siber lengkap (SEOJK 29/2022 Bab IX huruf b)','wajib disampaikan melalui sistem pelaporan OJK dalam 5 hari kerja.','\u2501'.repeat(45)].join('\n')
}
function generateIntelReport(t) {
  const entities=t.detected_entities?.entities||[], tags=(t.institution_tags||[]).join(', ')||'-', counts={}
  entities.forEach(e=>{counts[e.type]=(counts[e.type]||0)+1}); const reks=[],seen=new Set()
  entities.forEach(e=>{if(REKOMENDASI[e.type]&&!seen.has(e.type)){seen.add(e.type);reks.push(REKOMENDASI[e.type])}})
  return ['LAPORAN INTELIJEN INTERNAL \u2014 NusaShield FI','='.repeat(42),`Nomor          : INTEL-NSFI-${(t.id||'').slice(0,8).toUpperCase()}`,`Tanggal        : ${formatDateWib(t.created_at)}`,`Tingkat        : ${SEV_LABEL[t.severity]||t.severity}`,`Status         : ${STATUS_LABEL[t.status]||t.status}`,`Skor Risiko    : ${t.risk_score}/100`,`Sumber         : ${SRC_LABEL[t.source_type]||t.source_type}`,`URL            : ${t.source_url||'-'}`,`Lembaga Terkait: ${tags}`,'',`ENTITAS TERDETEKSI (${entities.length})`,'-'.repeat(36),...entities.map((e,i)=>`   ${i+1}. [${ENTITY_LABEL[e.type]||e.type}] ${e.value} (confidence: ${(e.confidence*100).toFixed(0)}%)`),'','DISTRIBUSI TIPE','-'.repeat(15),...Object.entries(counts).sort().map(([t,c])=>`   ${ENTITY_LABEL[t]||t}: ${c}`),'','REKOMENDASI TEKNIS','-'.repeat(18),...reks.slice(0,6).map((r,i)=>`   ${i+1}. ${r}`),'','INDIKATOR TEKNIS','-'.repeat(16),`   Hash konten     : ${t.content_hash||'-'}`,`   Preview tersamar: ${(t.content_preview||t.raw_content||'-').slice(0,200)}`,'','   CATATAN: Konten asli tidak disimpan sesuai prinsip minimisasi','   data (UU PDP Pasal 16).','','='.repeat(42),'Dokumen internal NusaShield FI. Tidak untuk distribusi eksternal.'].join('\n')
}
function buildRiskFactors(t) {
  const f=[], entities=t.detected_entities?.entities||[], types=sensitiveTypes(entities)
  if(entities.length>5)f.push({label:`Volume tinggi: ${entities.length} entitas`,color:'var(--sev-tinggi-bdr)',text:'var(--sev-tinggi-text)'})
  if(t.risk_score>=80)f.push({label:'Sumber: carding forum',color:'var(--sev-kritis-bdr)',text:'var(--sev-kritis-text)'})
  const age=(Date.now()-new Date(t.created_at).getTime())/3600000
  if(age<6)f.push({label:`Data segar: <${Math.ceil(age)} jam`,color:'var(--accent-border)',text:'var(--accent)'})
  if(types.length>=3)f.push({label:`Multi-entitas: ${types.join('+')}`,color:'rgba(124,58,237,0.2)',text:'#a78bfa'})
  if(!f.length)f.push({label:'Analisis standar',color:'var(--border-subtle)',text:'var(--text-muted)'})
  return f
}

export default function ThreatDetail({ threat: t, onClose }) {
  const [status,setStatus]=useState(t.status),[exportingOjk,setExportingOjk]=useState(false),[exportingIntel,setExportingIntel]=useState(false),[showTooltip,setShowTooltip]=useState(false)
  const mutation=useUpdateStatus(), entities=t.detected_entities?.entities||[], sv=SEV_VAR[t.severity]||SEV_VAR.LOW, isDemo=t._isDemo
  const rawPreview=t.content_preview||t.raw_content||t.raw_text_preview||'', factors=buildRiskFactors(t), entityTypes=sensitiveTypes(entities).filter(k=>REKOMENDASI[k])

  function handleStatusChange(v){setStatus(v);if(!isDemo)mutation.mutate({id:t.id,status:v})}
  async function handleExportOjk(){setExportingOjk(true);try{if(isDemo){dl(generateNotifikasiOJK(t),`DRAFT-NOTIFIKASI-OJK-${(t.id||'').slice(0,8)}`)}else{const r=await client.get(`/threats/${t.id}/report?format=ojk`);dl(r.data,`DRAFT-NOTIFIKASI-OJK-${(t.id||'').slice(0,8)}`)}}catch{}setExportingOjk(false)}
  async function handleExportIntel(){setExportingIntel(true);try{if(isDemo){dl(generateIntelReport(t),`INTEL-NSFI-${(t.id||'').slice(0,8)}`)}else{const r=await client.get(`/threats/${t.id}/report?format=intel`);dl(r.data,`INTEL-NSFI-${(t.id||'').slice(0,8)}`)}}catch{}setExportingIntel(false)}
  function dl(text,prefix){const d=new Date().toISOString().slice(0,10).replace(/-/g,''),b=new Blob([text],{type:'text/plain;charset=utf-8'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download=`${prefix}-${d}.txt`;a.click();URL.revokeObjectURL(u)}

  return (
    <>
      <div className="fixed inset-0 z-50" style={{backgroundColor:'var(--bg-overlay)'}} onClick={onClose} />
      <aside className="fixed top-0 right-0 h-full w-full max-w-[480px] z-50 overflow-y-auto"
        style={{backgroundColor:'var(--bg-card)',borderLeft:'1px solid var(--border-input)'}}>
        <div className="sticky top-0 px-6 py-4 flex items-center justify-between z-10"
          style={{backgroundColor:'var(--bg-header)',borderBottom:'1px solid var(--border-card)'}}>
          <div className="flex items-center gap-3">
            <svg width="18" height="18" viewBox="0 0 36 36" fill="none"><path d="M18 4 L30 28 Q24 26 18 28 Q12 26 6 28 Z" fill="var(--accent)" opacity="0.7" /></svg>
            <span className="px-2 py-0.5 rounded-md uppercase font-medium"
              style={{fontSize:'9px',letterSpacing:'0.06em',backgroundColor:`var(${sv.bg})`,color:`var(${sv.color})`,border:`1px solid var(${sv.border})`}}>
              {SEV_LABEL[t.severity]}
            </span>
            <div className="w-8 h-8 rounded-full flex items-center justify-center" style={{border:'2px solid var(--accent)',backgroundColor:'var(--score-bg)'}}>
              <span className="text-[11px] font-medium" style={{color:'var(--accent)'}}>{t.risk_score}</span>
            </div>
          </div>
          <button onClick={onClose} className="text-lg leading-none" style={{color:'var(--text-muted)'}}>&times;</button>
        </div>
        <div className="px-6 py-5 space-y-6">
          <section>
            <h2 className="text-base font-medium mb-1" style={{color:'var(--text-primary)'}}>
              {entities.length>0?`${ENTITY_LABEL[entities[0].type]||entities[0].type} via ${SRC_LABEL[t.source_type]||t.source_type}`:'Detail Ancaman'}
              {t.institution_tags?.length?` \u2014 ${t.institution_tags.join(', ')}`:''}
            </h2>
            {t.source_url&&<a href={t.source_url} target="_blank" rel="noopener noreferrer" className="text-xs truncate block" style={{color:'var(--tag-text)'}}>{t.source_url}</a>}
            <div className="flex items-center gap-3 mt-2">
              <span className="text-xs" style={{color:'var(--text-muted)'}}>{formatDate(t.created_at)}</span>
              <span className="px-2 py-0.5 rounded text-[10px] uppercase" style={{backgroundColor:'var(--accent-bg)',color:'var(--text-secondary)',border:'1px solid var(--border-subtle)'}}>
                {STATUS_LABEL[status]||status}
              </span>
            </div>
          </section>
          <section className="space-y-2">
            <Row label="ID" value={t.id} mono /><Row label="Sumber" value={SRC_LABEL[t.source_type]||t.source_type} />
            <Row label="Skor Risiko" value={`${t.risk_score} / 100`} accent /><Row label="Lembaga" value={(t.institution_tags||[]).join(', ')||'-'} />
          </section>
          <section>
            <SL>Entitas Terdeteksi ({entities.length})</SL>
            <div className="rounded-lg overflow-hidden" style={{border:'1px solid var(--border-card)'}}>
              <table className="w-full text-xs">
                <thead><tr style={{backgroundColor:'var(--accent-bg)'}}>
                  <th className="text-left px-3 py-2 font-medium" style={{color:'var(--text-muted)'}}>Tipe</th>
                  <th className="text-left px-3 py-2 font-medium" style={{color:'var(--text-muted)'}}>Nilai</th>
                  <th className="text-right px-3 py-2 font-medium" style={{color:'var(--text-muted)'}}>Confidence</th>
                </tr></thead>
                <tbody>{entities.map((e,i)=>{const conf=e.confidence||0;return(
                  <tr key={i} style={{backgroundColor:i%2===0?'transparent':'var(--bg-row-hover)',borderTop:'1px solid var(--border-divider)'}}>
                    <td className="px-3 py-2" style={{color:'var(--text-secondary)'}}>{ENTITY_LABEL[e.type]||e.type}</td>
                    <td className="px-3 py-2 font-mono" style={{color:'var(--accent)',fontSize:'11px'}}>{maskValue(e.value,e.type)}</td>
                    <td className="px-3 py-2"><div className="flex items-center justify-end gap-2">
                      <div className="w-14 h-1 rounded-full overflow-hidden" style={{backgroundColor:'var(--conf-track)'}}>
                        <div className="h-full rounded-full" style={{width:`${conf*100}%`,backgroundColor:'var(--accent)'}} /></div>
                      <span style={{color:'var(--text-secondary)'}}>{(conf*100).toFixed(0)}%</span></div></td>
                  </tr>)})}
                  {!entities.length&&<tr><td colSpan={3} className="px-3 py-4 text-center" style={{color:'var(--text-faint)'}}>Tidak ada entitas.</td></tr>}
                </tbody>
              </table>
            </div>
          </section>
          {rawPreview&&<section><SL>Cuplikan Konten (Tersamar)</SL>
            <div className="rounded-lg p-3 font-mono text-[11px] leading-relaxed overflow-hidden"
              style={{backgroundColor:'var(--bg-input)',border:'1px solid var(--border-subtle)',color:'var(--text-muted)',maxHeight:'4.5em',WebkitLineClamp:3,display:'-webkit-box',WebkitBoxOrient:'vertical'}}>{rawPreview}</div>
            <p className="text-[10px] mt-1" style={{color:'var(--text-faint)'}}>Konten ditampilkan dalam bentuk tersamar sesuai UU PDP.</p>
          </section>}
          <section><SL>Faktor Risiko</SL><div className="flex flex-wrap gap-2">
            {factors.map(f=><span key={f.label} className="text-[10px] px-2 py-1 rounded-md" style={{backgroundColor:f.color,color:f.text,border:`1px solid ${f.color}`}}>{f.label}</span>)}
          </div></section>
          {entityTypes.length>0&&<section><SL>Rekomendasi</SL>
            <ol className="space-y-2 list-decimal list-inside text-xs leading-relaxed" style={{color:'var(--text-secondary)'}}>
              {entityTypes.slice(0,4).map((k,i)=><li key={i}>{REKOMENDASI[k]}</li>)}</ol></section>}
          <section><SL>Status</SL>
            <select value={status} onChange={e=>handleStatusChange(e.target.value)} disabled={mutation.isPending} className="w-full px-3 py-2 rounded-lg text-sm"
              style={{backgroundColor:'var(--bg-input)',border:'1px solid var(--border-input)',color:'var(--text-secondary)',outline:'none'}}>
              {Object.entries(STATUS_LABEL).map(([k,v])=><option key={k} value={k} style={{backgroundColor:'var(--bg-input)'}}>{v}</option>)}</select>
            {mutation.isPending&&<p className="text-xs mt-1" style={{color:'var(--text-faint)'}}>Menyimpan...</p>}
          </section>
          <section className="space-y-3">
            <div className="relative">
              <button onClick={handleExportOjk} disabled={exportingOjk} className="w-full py-2.5 rounded-lg text-sm font-medium flex items-center justify-center gap-2"
                style={{border:'1px solid var(--accent-border)',color:'var(--accent)',backgroundColor:'transparent'}}
                onMouseEnter={e=>{e.currentTarget.style.backgroundColor='var(--accent-bg)';setShowTooltip(true)}}
                onMouseLeave={e=>{e.currentTarget.style.backgroundColor='transparent';setShowTooltip(false)}}>
                {exportingOjk?<><span className="w-3 h-3 border border-current border-t-transparent rounded-full animate-spin"/>Mengunduh...</>:'Siapkan Draft Notifikasi OJK'}</button>
              {showTooltip&&<div className="absolute bottom-full left-0 right-0 mb-2 px-3 py-2 rounded-lg text-[10px] leading-relaxed"
                style={{backgroundColor:'var(--bg-header)',border:'1px solid var(--border-input)',color:'var(--text-secondary)'}}>
                Draft notifikasi awal mengacu elemen wajib SEOJK 29/SEOJK.03/2022 Bab IX. Wajib disampaikan ke OJK dalam 24 jam setelah insiden dikonfirmasi.</div>}
            </div>
            <button onClick={handleExportIntel} disabled={exportingIntel} className="w-full py-2.5 rounded-lg text-sm font-medium flex items-center justify-center gap-2"
              style={{border:'1px solid var(--border-subtle)',color:'var(--text-secondary)',backgroundColor:'transparent'}}
              onMouseEnter={e=>(e.currentTarget.style.backgroundColor='var(--bg-row-hover)')}
              onMouseLeave={e=>(e.currentTarget.style.backgroundColor='transparent')}>
              {exportingIntel?<><span className="w-3 h-3 border border-current border-t-transparent rounded-full animate-spin"/>Mengunduh...</>:'Laporan Intelijen Lengkap'}</button>
          </section>
        </div>
      </aside>
    </>
  )
}
function SL({children}){return<h3 className="text-[11px] uppercase tracking-wider mb-2" style={{color:'var(--text-muted)',letterSpacing:'0.06em'}}>{children}</h3>}
function Row({label,value,mono=false,accent=false}){return<div className="flex text-sm"><dt className="w-28 shrink-0" style={{color:'var(--text-muted)'}}>{label}</dt><dd className={`min-w-0 truncate ${mono?'font-mono text-xs mt-0.5':''}`} style={{color:accent?'var(--accent)':'var(--text-primary)'}}>{value}</dd></div>}
