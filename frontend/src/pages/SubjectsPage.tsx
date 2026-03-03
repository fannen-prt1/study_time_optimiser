import { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import {
  fetchSubjects,
  createSubject,
  updateSubject,
  deleteSubject,
  archiveSubject,
  unarchiveSubject,
} from '../store/slices/subjectsSlice';
import type { Subject, CreateSubjectRequest } from '../types';
import toast from 'react-hot-toast';

const PRESET_COLORS = [
  '#6366f1', // indigo
  '#8b5cf6', // violet
  '#ec4899', // pink
  '#ef4444', // red
  '#f97316', // orange
  '#eab308', // yellow
  '#22c55e', // green
  '#14b8a6', // teal
  '#06b6d4', // cyan
  '#3b82f6', // blue
  '#6b7280', // gray
  '#a855f7', // purple
];

export function SubjectsPage() {
  const dispatch = useAppDispatch();
  const { subjects, isLoading } = useAppSelector((state) => state.subjects);
  const [showModal, setShowModal] = useState(false);
  const [editingSubject, setEditingSubject] = useState<Subject | null>(null);
  const [showArchived, setShowArchived] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

  // Form state
  const [formData, setFormData] = useState<CreateSubjectRequest>({
    name: '',
    color: PRESET_COLORS[0],
    description: '',
  });

  useEffect(() => {
    dispatch(fetchSubjects(showArchived));
  }, [dispatch, showArchived]);

  const activeSubjects = subjects.filter((s) => !s.is_archived);
  const archivedSubjects = subjects.filter((s) => s.is_archived);

  const openCreateModal = () => {
    setEditingSubject(null);
    setFormData({ name: '', color: PRESET_COLORS[0], description: '' });
    setShowModal(true);
  };

  const openEditModal = (subject: Subject) => {
    setEditingSubject(subject);
    setFormData({
      name: subject.name,
      color: subject.color,
      description: subject.description || '',
    });
    setShowModal(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name.trim()) {
      toast.error('Subject name is required');
      return;
    }

    try {
      if (editingSubject) {
        await dispatch(updateSubject({ id: editingSubject.id, data: formData })).unwrap();
        toast.success('Subject updated!');
      } else {
        await dispatch(createSubject(formData)).unwrap();
        toast.success('Subject created!');
      }
      setShowModal(false);
    } catch (err) {
      toast.error(typeof err === 'string' ? err : 'Something went wrong');
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await dispatch(deleteSubject(id)).unwrap();
      toast.success('Subject deleted');
      setDeleteConfirm(null);
    } catch (err) {
      toast.error(typeof err === 'string' ? err : 'Failed to delete');
    }
  };

  const handleArchive = async (id: string) => {
    try {
      await dispatch(archiveSubject(id)).unwrap();
      toast.success('Subject archived');
    } catch (err) {
      toast.error(typeof err === 'string' ? err : 'Failed to archive');
    }
  };

  const handleUnarchive = async (id: string) => {
    try {
      await dispatch(unarchiveSubject(id)).unwrap();
      toast.success('Subject unarchived');
    } catch (err) {
      toast.error(typeof err === 'string' ? err : 'Failed to unarchive');
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Subjects</h1>
          <p className="text-sm text-[#7a96b0] mt-0.5">Manage your study subjects and categories</p>
        </div>
        <button
          onClick={openCreateModal}
          className="inline-flex items-center gap-2 px-4 py-2.5 bg-primary text-white rounded-lg shadow-sm hover:bg-primary/90 transition-colors font-bold text-sm"
        >
          <span className="material-symbols-outlined text-lg">add</span>
          Add Subject
        </button>
      </div>

      {/* Active Subjects Grid */}
      {isLoading && subjects.length === 0 ? (
        <div className="flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-10 w-10 border-[3px] border-[#233648] border-t-primary" />
        </div>
      ) : activeSubjects.length === 0 ? (
        <div className="rounded-xl border border-[#233648] bg-[#0F172A] p-14 text-center">
          <span className="material-symbols-outlined text-slate-300 text-5xl mb-3">menu_book</span>
          <h3 className="text-base font-bold text-white mb-1">No subjects yet</h3>
          <p className="text-sm text-[#7a96b0] mb-5">Create your first subject to start tracking study time</p>
          <button
            onClick={openCreateModal}
            className="inline-flex items-center gap-2 px-4 py-2.5 bg-primary text-white rounded-lg shadow-sm hover:bg-primary/90 font-bold text-sm"
          >
            <span className="material-symbols-outlined text-lg">add</span>
            Create Subject
          </button>
        </div>
      ) : (
        <>
          <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-3">Active Subjects ({activeSubjects.length})</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {activeSubjects.map((subject) => (
              <div key={subject.id} className="rounded-xl border border-[#233648] bg-[#0F172A] overflow-hidden hover:shadow-card transition-shadow">
                {/* Color bar */}
                <div className="h-1.5" style={{ backgroundColor: subject.color }} />
                <div className="p-5">
                  <div className="flex items-start gap-3 mb-4">
                    <div className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0" style={{ backgroundColor: subject.color + '20' }}>
                      <span className="material-symbols-outlined text-xl" style={{ color: subject.color }}>menu_book</span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-bold text-white truncate">{subject.name}</h3>
                      {subject.description && (
                        <p className="text-xs text-[#7a96b0] mt-0.5 line-clamp-2">{subject.description}</p>
                      )}
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-1 pt-3 border-t border-[#233648]">
                    <button
                      onClick={() => openEditModal(subject)}
                      className="p-2 text-[#4a6580] hover:text-primary hover:bg-primary/10 rounded-lg transition-colors"
                      title="Edit"
                    >
                      <span className="material-symbols-outlined text-lg">edit</span>
                    </button>
                    <button
                      onClick={() => handleArchive(subject.id)}
                      className="p-2 text-[#4a6580] hover:text-amber-500 hover:bg-amber-900/20 rounded-lg transition-colors"
                      title="Archive"
                    >
                      <span className="material-symbols-outlined text-lg">inventory_2</span>
                    </button>
                    {deleteConfirm === subject.id ? (
                      <div className="flex items-center gap-1 ml-auto">
                        <span className="text-xs text-rose-600 mr-1">Delete?</span>
                        <button
                          onClick={() => handleDelete(subject.id)}
                          className="px-2 py-1 text-xs bg-rose-500 text-white rounded-lg hover:bg-rose-600 font-bold"
                        >
                          Yes
                        </button>
                        <button
                          onClick={() => setDeleteConfirm(null)}
                          className="px-2 py-1 text-xs border border-[#233648] text-slate-300 rounded-lg hover:bg-[#102337] font-medium"
                        >
                          No
                        </button>
                      </div>
                    ) : (
                      <button
                        onClick={() => setDeleteConfirm(subject.id)}
                        className="p-2 text-[#4a6580] hover:text-rose-500 hover:bg-rose-900/20 rounded-lg transition-colors ml-auto"
                        title="Delete"
                      >
                        <span className="material-symbols-outlined text-lg">delete</span>
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {/* Archived Subjects */}
      {archivedSubjects.length > 0 && (
        <div className="mt-8">
          <button
            onClick={() => setShowArchived(!showArchived)}
            className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#7a96b0] hover:text-white mb-4 transition-colors"
          >
            <span className="material-symbols-outlined text-lg">inventory_2</span>
            {showArchived ? 'Hide' : 'Show'} archived ({archivedSubjects.length})
            <span className="material-symbols-outlined text-sm">{showArchived ? 'expand_less' : 'expand_more'}</span>
          </button>

          {showArchived && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {archivedSubjects.map((subject) => (
                <div key={subject.id} className="rounded-xl border border-[#233648] bg-[#102337] overflow-hidden opacity-75">
                  <div className="h-1.5 bg-slate-300" />
                  <div className="p-5">
                    <div className="flex items-center gap-3 mb-4">
                      <div className="w-10 h-10 rounded-xl bg-slate-200 flex items-center justify-center">
                        <span className="material-symbols-outlined text-[#4a6580] text-xl">menu_book</span>
                      </div>
                      <div>
                        <h3 className="font-bold text-[#7a96b0]">{subject.name}</h3>
                        <span className="text-xs text-[#4a6580]">Archived</span>
                      </div>
                    </div>
                    <div className="pt-3 border-t border-[#233648]">
                      <button
                        onClick={() => handleUnarchive(subject.id)}
                        className="flex items-center gap-1.5 text-xs font-bold text-primary hover:text-primary/80 transition-colors"
                      >
                        <span className="material-symbols-outlined text-sm">unarchive</span>
                        Restore
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Create/Edit Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#102337] rounded-xl border border-[#233648] shadow-xl w-full max-w-md">
            <div className="flex items-center justify-between px-6 py-4 border-b border-[#233648]">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-primary">menu_book</span>
                <h2 className="text-base font-bold text-white">
                  {editingSubject ? 'Edit Subject' : 'New Subject'}
                </h2>
              </div>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white transition-colors">
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Subject Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none text-sm text-white bg-[#102337]"
                  placeholder="e.g., Mathematics, Physics, History..."
                  autoFocus
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Description</label>
                <textarea
                  value={formData.description || ''}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none resize-none text-sm text-white bg-[#102337]"
                  rows={2}
                  placeholder="Brief description of this subject..."
                />
              </div>

              {/* Color Picker */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-2">Color</label>
                <div className="flex flex-wrap gap-2">
                  {PRESET_COLORS.map((color) => (
                    <button
                      key={color}
                      type="button"
                      onClick={() => setFormData({ ...formData, color })}
                      className={`w-7 h-7 rounded-full border-2 transition-transform hover:scale-110 ${
                        formData.color === color ? 'border-slate-900 scale-110' : 'border-transparent'
                      }`}
                      style={{ backgroundColor: color }}
                    />
                  ))}
                </div>
              </div>

              {/* Preview */}
              <div className="bg-[#102337] rounded-xl border border-[#233648] p-3">
                <p className="text-[10px] font-bold uppercase tracking-wider text-[#4a6580] mb-2">Preview</p>
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: formData.color + '20' }}>
                    <span className="material-symbols-outlined text-lg" style={{ color: formData.color }}>menu_book</span>
                  </div>
                  <span className="font-bold text-white text-sm">{formData.name || 'Subject Name'}</span>
                </div>
              </div>

              <div className="flex gap-3 pt-1">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 px-4 py-2.5 border border-[#233648] text-slate-300 rounded-lg hover:bg-[#102337] transition-colors font-medium text-sm"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="flex-1 px-4 py-2.5 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors font-bold text-sm disabled:opacity-50 shadow-sm"
                >
                  {isLoading ? 'Saving...' : editingSubject ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

